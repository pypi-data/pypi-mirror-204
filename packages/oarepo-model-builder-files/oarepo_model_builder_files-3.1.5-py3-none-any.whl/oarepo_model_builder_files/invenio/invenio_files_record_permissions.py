from oarepo_model_builder_files.invenio.invenio_files import InvenioFilesClassPythonBuilder


class InvenioFilesRecordPermissionsBuilder(InvenioFilesClassPythonBuilder):
    TYPE = "invenio_files_permissions"
    class_config = "record-permissions-class"
    template = "files-permissions"