#
# Copyright (C) 2013 - 2023 Oracle and/or its affiliates. All rights reserved.
#

from pypgx._utils.error_handling import java_handler

from pypgx.api.mllib._input_property_config import InputPropertyConfig


class CategoricalPropertyConfig(InputPropertyConfig):
    """Configuration class for handling categorical input properties."""

    _java_class = "oracle.pgx.config.mllib.inputconfig.CategoricalPropertyConfig"

    def __init__(self, java_config, params) -> None:
        super().__init__(java_config, params)
        self._config = java_config
        self.params = params

    @property
    def shared(self) -> bool:
        """Get whether the feature is shared among vertex/edge types.

        :return: whether the feature is shared among vertex/edge types
        """
        return java_handler(self._config.getShared, [])

    @property
    def max_vocabulary_size(self) -> bool:
        """Get the maximum number of tokens allowed in the vocabulary of a categorical feature.
        The most frequent category values numbering max_vocabulary_size are kept,
        the rest are treated as OOV tokens.

        :return: maximum number of tokens allowed
        """
        return java_handler(self._config.getMaxVocabularySize, [])

    @property
    def categorical_embedding_type(self) -> bool:
        """Get the type of categorical embedding.

        :return: type of categorical embedding
        """
        return java_handler(self._config.getCategoricalEmbeddingType, [])

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
