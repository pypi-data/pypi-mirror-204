from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.jinja import package_name

class InvenioFilesClassPythonBuilder(InvenioBaseClassPythonBuilder):
    MODULE = None

    def get_module(self):
        return package_name(self.current_model[self.class_config])

    def finish(self, **extra_kwargs):
        module = self.MODULE if self.MODULE else self.get_module()
        python_path = self.module_to_path(module)
        self.process_template(
            python_path,
            self.template,
            current_package_name=module,
            files=self.schema.files,
            model=self.schema.model,
            **extra_kwargs,
        )
