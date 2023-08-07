from oarepo_model_builder.model_preprocessors import ModelPreprocessor
from oarepo_model_builder.utils.camelcase import camel_case

class InvenioModelFilesBaseClassesPreprocessor(ModelPreprocessor):
    TYPE = "invenio_files_base_classes"

    def transform(self, schema, settings):
        model = schema.current_model
        self.set_default_and_prepend_if_not_present(model, "record-metadata-bases", [],
                                                   "invenio_records_resources.records.FileRecordModelMixin")