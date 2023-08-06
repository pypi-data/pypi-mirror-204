#
# Copyright (C) 2013 - 2023 Oracle and/or its affiliates. All rights reserved.
#

from pypgx._utils.error_handling import java_handler

from pypgx.api.mllib._categorical_property_config import CategoricalPropertyConfig


class EmbeddingTableConfig(CategoricalPropertyConfig):
    """Configuration class for handling categorical input properties
    using embedding table method.
    """

    _java_class = "oracle.pgx.config.mllib.inputconfig.EmbeddingTableConfig"

    def __init__(self, java_config, params) -> None:
        super().__init__(java_config, params)
        self._config = java_config
        self.params = params

    @property
    def embedding_dim(self) -> int:
        """Get the embedding dimension.

        :return: embedding dimension
        """
        return java_handler(self._config.getEmbeddingDimension, [])

    @property
    def oov_probability(self) -> float:
        """Get the probability of randomly setting the category value
        to OOV token during training.

        :return: probability of using OOV token
        """
        return java_handler(self._config.getOutOfVocabularyProbability, [])

    def __repr__(self) -> str:
        attributes = []
        for param in self.params:
            if param != "self":
                attributes.append("%s: %s" % (param, self.params[param]))
        return "%s(%s)" % (self.__class__.__name__, ", ".join(attributes))

    def __str__(self) -> str:
        return repr(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._config.equals(other._config)
