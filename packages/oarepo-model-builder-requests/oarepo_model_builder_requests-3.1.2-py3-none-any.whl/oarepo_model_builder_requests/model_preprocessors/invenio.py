from oarepo_model_builder.model_preprocessors import ModelPreprocessor
from oarepo_model_builder.utils.camelcase import camel_case


class InvenioModelPreprocessor(ModelPreprocessor):
    TYPE = "invenio_requests"

    def transform(self, schema, settings):
        model = schema.current_model
        self.set(
            model,
            "requests-package",
            lambda: f"{model.package}.requests",
        )

        self.set(
            model,
            "requests-record-resolver-class",
            lambda: f"{model.requests_package}.resolvers.{model.record_prefix}Resolver",
        )

        self.set(
            model,
            "requests-types",
            lambda: f"{model.requests_package}.types",
        )

        self.set(
            model,
            "requests-actions",
            lambda: f"{model.requests_package}.actions",
        )
        # requests

        requests = getattr(schema.schema, "requests", {})
        for request_name, request_data in requests.items():
            request_data.setdefault(
                "class",
                f"{model.requests_types}.{camel_case(request_name)}RequestType",
            )
            request_data.setdefault("generate", True)
            request_data.setdefault(
                "bases", ["invenio_requests.customizations.RequestType"]
            )  # accept action
            # this needs to be updated if other types of actions are considered
            request_data.setdefault("actions", {"approve": {}})
            for action_name, action_data in request_data.actions.items():
                action_data.setdefault(
                    "class",
                    f"{model.requests_actions}.{camel_case(request_name)}RequestAcceptAction",
                )
                action_data.setdefault("generate", True)
                action_data.setdefault(
                    "bases", ["invenio_requests.customizations.AcceptAction"]
            )

        print()
