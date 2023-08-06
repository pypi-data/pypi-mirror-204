import marshmallow as ma
from marshmallow import fields
from oarepo_model_builder.validation.utils import RegexFieldsSchema

class ActionSchema(ma.Schema):
    action_class = fields.String(data_key="class", required=False)
    bases = fields.List(fields.String, required=False)
    generate = fields.Boolean(required=False)
    class Meta:
        unknown = ma.RAISE
class ActionsSchema(ma.Schema):
    approve = fields.Nested(ActionSchema)
    class Meta:
        unknown = ma.RAISE
class RequestTypeSchema(ma.Schema):
    type_class = fields.String(data_key="class", required=False)
    bases = fields.List(fields.String, required=False)
    generate = fields.Boolean(required=False)
    actions = fields.Nested(ActionsSchema)
    class Meta:
        unknown = ma.RAISE

class RequestsSchema(RegexFieldsSchema):
    class Meta:
        regex_fields = [
            {
                "key": "^.*$",
                "field": lambda: fields.Nested(
                    RequestTypeSchema
                ),
            },
        ]
class RequestsBaseSchema(ma.Schema):
    requests = fields.Nested(RequestsSchema)


class RequestsModelSchema(ma.Schema):
    requests_package = fields.String(data_key="requests-package")
    requests_record_resolver_class = fields.String(data_key="requests-record-resolver-class")
    requests_types = fields.String(data_key="requests-types")
    requests_actions = fields.String(data_key="requests-actions")



validators = {"root": RequestsBaseSchema, "model": RequestsModelSchema}