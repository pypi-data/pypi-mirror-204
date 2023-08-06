from oarepo_model_builder_requests.invenio.invenio_requests_builder import InvenioRequestsPythonBuilder


class InvenioRequestsConfigBuilder(InvenioRequestsPythonBuilder):
    TYPE = "invenio_requests_config"
    template = "requests-config"

    def get_module(self):
        return self.current_model.config_package