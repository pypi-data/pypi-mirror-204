import copy

from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch


class InvenioRequestsPythonBuilder(InvenioBaseClassPythonBuilder):
    MODULE = None

    def get_module(self):
        return self.current_model.requests_package
    def process_request_data(self):
        requests = copy.deepcopy(getattr(self.schema, "requests", {}))
        request_jinjadata = HyphenMunch()
        for request_name, request_data in requests.items():
            cur_request_jinjadata = HyphenMunch()
            cur_request_jinjadata["type-class"] = request_data["class"]
            cur_request_jinjadata["type-bases"] = request_data["bases"]
            cur_request_jinjadata["type-generate"] = request_data["generate"]
            approve_action_data = request_data.actions.approve
            cur_request_jinjadata["approve-action-class"] = approve_action_data["class"]
            cur_request_jinjadata["approve-action-bases"] = approve_action_data["bases"]
            cur_request_jinjadata["approve-action-generate"] = approve_action_data["generate"]
            request_jinjadata[request_name] = cur_request_jinjadata
        return request_jinjadata


    def finish(self, **extra_kwargs):
        requests = self.process_request_data()
        module = self.MODULE if self.MODULE else self.get_module()
        python_path = self.module_to_path(module)
        self.process_template(
            python_path,
            self.template,
            current_package_name=module,
            requests=requests,
            **extra_kwargs,
        )