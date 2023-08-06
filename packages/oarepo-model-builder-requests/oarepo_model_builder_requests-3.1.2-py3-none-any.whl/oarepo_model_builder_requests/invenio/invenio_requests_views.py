from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.jinja import package_name


class InvenioRequestsViewsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_views"
    template = "requests-views"
    class_config = "create_blueprint_from_app"

