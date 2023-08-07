from oarepo_model_builder_files.invenio.invenio_files import InvenioFilesClassPythonBuilder


class InvenioFilesSchemaBuilder(InvenioFilesClassPythonBuilder):
    TYPE = "invenio_files_schema"
    class_config = "record-schema-class"
    template = "files-schema"