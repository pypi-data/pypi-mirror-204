from oarepo_model_builder_requests.invenio.invenio_requests_builder import InvenioRequestsPythonBuilder


class InvenioRequestsConftestBuilder(InvenioRequestsPythonBuilder):
    TYPE = "invenio_requests_conftest"
    template = "requests-conftest"
    MODULE = "tests.requests.conftest"

