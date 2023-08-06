from oarepo_model_builder_requests.invenio.invenio_requests_builder import InvenioRequestsPythonBuilder


class InvenioRequestsActionsBuilder(InvenioRequestsPythonBuilder):
    TYPE = "invenio_requests_actions"
    template = "requests-actions"

    def get_module(self):
        return self.current_model.requests_actions


