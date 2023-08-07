from oarepo_model_builder.utils.jinja import package_name
from oarepo_model_builder_files.invenio.invenio_files import InvenioFilesClassPythonBuilder


class InvenioFilesParentRecordServiceConfigBuilder(InvenioFilesClassPythonBuilder):
    TYPE = "invenio_files_parent_record_service_config"
    class_config = "record-service-config-class"
    template = "files-parent-record-service-config"

    def get_module(self):
        return package_name(self.schema.model[self.class_config]) #use parent class path
