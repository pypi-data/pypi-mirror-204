from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.jinja import package_name


class InvenioRequestsResolversBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_resolvers"
    class_config = "requests-record-resolver-class"
    template = "requests-resolvers"

