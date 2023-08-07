from oarepo_model_builder_files.invenio.invenio_files import InvenioFilesClassPythonBuilder


class InvenioFilesTestFileResourcesBuilder(InvenioFilesClassPythonBuilder):
    TYPE = "invenio_files_test_files_resources"
    template = "files-test-file-resources"
    MODULE = "tests.files.test_files_resources"
