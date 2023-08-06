from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.outputs.cfg import CFGOutput


class InvenioRequestsSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_requests_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")
        if getattr(self.schema, "requests", None):
            output.add_dependency("invenio-requests", ">=1.0.2")
