

from oarepo_model_builder_files.invenio.invenio_files import InvenioFilesClassPythonBuilder


class InvenioFilesRecordBuilder(InvenioFilesClassPythonBuilder):
    TYPE = "invenio_files_record"
    class_config = "record-class"
    template = "files-record"

