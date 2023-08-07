from oarepo_model_builder_files.invenio.invenio_files import InvenioFilesClassPythonBuilder


class InvenioRecordServiceConfigBuilder(InvenioFilesClassPythonBuilder):
    TYPE = "invenio_files_record_service_config"
    class_config = "record-service-config-class"
    template = "files-service-config"
