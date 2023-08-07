from oarepo_model_builder_files.invenio.invenio_files import InvenioFilesClassPythonBuilder

class InvenioConftestBuilder(InvenioFilesClassPythonBuilder):
    TYPE = "conftest"
    template = "invenio-conftest"
    MODULE = "tests.conftest"