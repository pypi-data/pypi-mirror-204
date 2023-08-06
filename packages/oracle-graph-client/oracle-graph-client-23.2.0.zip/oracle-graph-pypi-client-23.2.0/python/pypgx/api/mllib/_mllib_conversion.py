#
# Copyright (C) 2013 - 2023 Oracle and/or its affiliates. All rights reserved.
#
from typing import Dict
from jnius import cast

from pypgx._utils import conversion
from pypgx.api.mllib._input_property_config import InputPropertyConfig
from pypgx.api.mllib._one_hot_encoding_config import OneHotEncodingConfig
from pypgx.api.mllib._embedding_table_config import EmbeddingTableConfig
from pypgx.api.mllib._continuous_property_config import ContinuousFeatureConfig


def _java_input_property_list_to_python_configs(java_input_property_configs_map) -> \
        Dict[str, InputPropertyConfig]:
    input_property_configs: Dict[str, InputPropertyConfig] = {}
    for prop_name, java_config in conversion.map_to_python(java_input_property_configs_map).items():
        if java_config.getCategorical():
            config = cast(
                'oracle.pgx.config.mllib.inputconfig.CategoricalPropertyConfig', java_config
            )
            embedding_type = conversion.enum_to_python_str(config.getCategoricalEmbeddingType())
            if embedding_type == "one_hot_encoding":
                config = cast('oracle.pgx.config.mllib.inputconfig.OneHotEncodingConfig', config)
                input_property_configs[prop_name] = OneHotEncodingConfig(config, {})
            elif embedding_type == "embedding_table":
                config = cast('oracle.pgx.config.mllib.inputconfig.EmbeddingTableConfig', config)
                input_property_configs[prop_name] = EmbeddingTableConfig(config, {})
            else:
                raise ValueError("Type of the InputPropertyConfig not recognized")
        else:
            config = cast(
                'oracle.pgx.config.mllib.inputconfig.ContinuousPropertyConfig', java_config
            )
            input_property_configs[prop_name] = ContinuousFeatureConfig(config, {})
    return input_property_configs
