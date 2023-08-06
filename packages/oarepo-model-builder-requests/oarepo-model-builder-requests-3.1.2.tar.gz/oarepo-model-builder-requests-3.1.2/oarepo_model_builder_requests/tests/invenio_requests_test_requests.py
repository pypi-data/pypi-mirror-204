from oarepo_model_builder_requests.invenio.invenio_requests_builder import InvenioRequestsPythonBuilder


class InvenioRequestsTestRequestsBuilder(InvenioRequestsPythonBuilder):
    TYPE = "invenio_requests_tests"
    template = "requests-tests"
    MODULE = "tests.requests.test_requests"
