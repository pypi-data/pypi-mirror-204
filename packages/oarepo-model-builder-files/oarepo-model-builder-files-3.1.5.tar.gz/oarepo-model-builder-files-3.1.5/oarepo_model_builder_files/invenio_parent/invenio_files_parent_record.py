from oarepo_model_builder.utils.jinja import package_name
from oarepo_model_builder_files.invenio.invenio_files import InvenioFilesClassPythonBuilder


class InvenioFilesParentRecordBuilder(InvenioFilesClassPythonBuilder):
    TYPE = "invenio_files_parent_record"
    class_config = "record-class"
    template = "files-parent-record"

    def get_module(self):
        return package_name(self.schema.model[self.class_config]) #use parent class path

