from oarepo_model_builder.utils.jinja import package_name
from oarepo_model_builder_files.invenio.invenio_files import InvenioFilesClassPythonBuilder


class InvenioFilesParentSchemaBuilder(InvenioFilesClassPythonBuilder):
    TYPE = "invenio_files_parent_schema"
    class_config = "record-schema-class"
    template = "files-parent-schema"

    def get_module(self):
        return package_name(self.schema.model[self.class_config]) #use parent class path
