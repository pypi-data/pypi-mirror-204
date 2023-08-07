from oarepo_model_builder.model_preprocessors import ModelPreprocessor
from oarepo_model_builder.utils.camelcase import camel_case

class InvenioModelFilesBeforePreprocessor(ModelPreprocessor):
    TYPE = "invenio_files_before"

    def transform(self, schema, settings):
        files = schema.schema.files
        model = schema.schema.model

        parent_record_prefix = camel_case(
                        model.package.rsplit(".", maxsplit=1)[-1]
                    )
        files.setdefault("record-prefix", f"{parent_record_prefix}File")
        files.setdefault("record-permissions-class", model.record_permissions_class)
        files.setdefault("profile-package", "files")
        files.setdefault("record-service-config-generate-links", False)
        files.setdefault("collection-url", f'{model["collection-url"]}<pid_value>')

        files.setdefault("record-resource-parent-class", "invenio_records_resources.resources.files.resource.FileResource")
        files.setdefault("record-resource-config-parent-class", "invenio_records_resources.resources.FileResourceConfig")
        files.setdefault("record-service-parent-class", "invenio_records_resources.services.FileService")
        files.setdefault("record-service-config-parent-class", "invenio_records_resources.services.FileServiceConfig")
        files.setdefault("record-parent-class", "invenio_records_resources.records.api.FileRecord")


        model.setdefault("record-service-config-components", []).append("invenio_records_resources.services.records.components.FilesOptionsComponent")