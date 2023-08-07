from oarepo_model_builder_files.invenio.invenio_files import InvenioFilesClassPythonBuilder


class InvenioFilesRecordMetadataBuilder(InvenioFilesClassPythonBuilder):
    TYPE = "invenio_files_record_metadata"
    class_config = "record-metadata-class"
    template = "files-record-metadata"
