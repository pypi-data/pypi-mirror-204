import marshmallow as ma
from marshmallow import fields
from oarepo_model_builder.validation.model_validation import model_validator


class FilesModelSchema(ma.Schema):
    files = fields.Nested(lambda: model_validator.validator_class("model")())


validators = {"root": FilesModelSchema}
