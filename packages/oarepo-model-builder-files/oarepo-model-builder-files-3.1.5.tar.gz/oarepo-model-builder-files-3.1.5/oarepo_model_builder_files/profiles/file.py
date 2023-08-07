import copy
from pathlib import Path
from typing import Union

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.conflict_resolvers import AutomaticResolver
from oarepo_model_builder.entrypoints import create_builder_from_entrypoints
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.profiles import Profile

from oarepo_model_builder.utils.hyphen_munch import HyphenMunch
import munch


class FileProfile(Profile):
    # schema - ideas - build new schema from specifications of the submodel??
    # but I still probably need some of the old settings in the new schema and this would overwrite them?
    #
    # required_profiles = ('model',)
    def build(
            self,
            model: ModelSchema,
            output_directory: Union[str, Path],
            builder: ModelBuilder,
    ):
        original_model_preprocessors = [model_preprocessor for model_preprocessor in builder.model_preprocessor_classes
                                        if "oarepo_model_builder." in str(model_preprocessor)]
        builder._validate_model(model)
        for model_preprocessor in original_model_preprocessors:
            model_preprocessor(builder).transform(model, model.settings)

        model.model_field = "files"
        builder.build(model, output_directory)