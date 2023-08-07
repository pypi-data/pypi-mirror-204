from oarepo_model_builder_files.invenio.invenio_files import InvenioFilesClassPythonBuilder


class InvenioFilesConftestBuilder(InvenioFilesClassPythonBuilder):
    TYPE = "invenio_files_conftest"
    template = "files-conftest"
    MODULE = "tests.files.conftest"
