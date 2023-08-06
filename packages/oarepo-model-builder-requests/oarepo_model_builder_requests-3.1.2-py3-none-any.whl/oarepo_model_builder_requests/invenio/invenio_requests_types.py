from oarepo_model_builder_requests.invenio.invenio_requests_builder import InvenioRequestsPythonBuilder


class InvenioRequestsTypesBuilder(InvenioRequestsPythonBuilder):
    TYPE = "invenio_requests_types"
    template = "requests-types"

    def get_module(self):
        return self.current_model.requests_types


