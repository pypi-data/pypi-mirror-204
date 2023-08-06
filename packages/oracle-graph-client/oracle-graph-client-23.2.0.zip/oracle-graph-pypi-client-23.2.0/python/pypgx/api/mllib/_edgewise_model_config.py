#
# Copyright (C) 2013 - 2023 Oracle and/or its affiliates. All rights reserved.
#

from typing import List, Dict

from pypgx._utils.error_handling import java_handler
from pypgx._utils import conversion
from pypgx.api.mllib._graphwise_conv_layer_config import GraphWiseConvLayerConfig
from pypgx.api.mllib._input_property_config import InputPropertyConfig
from pypgx.api.mllib._mllib_conversion import _java_input_property_list_to_python_configs


class EdgeWiseModelConfig:
    """Edgewise Model Configuration class"""

    _java_class = 'oracle.pgx.config.mllib.EdgeWiseModelConfig'

    def __init__(self, java_edgewise_model_config) -> None:
        self._config = java_edgewise_model_config
        self.shuffle = java_edgewise_model_config.isShuffle()
        self.input_feature_dim = java_edgewise_model_config.getInputFeatureDim()
        self.edge_input_feature_dim = java_edgewise_model_config.getEdgeInputFeatureDim()
        self.is_fitted = java_edgewise_model_config.isFitted()
        self.training_loss = java_edgewise_model_config.getTrainingLoss()
        self.batch_size = java_edgewise_model_config.getBatchSize()
        self.num_epochs = java_edgewise_model_config.getNumEpochs()
        self.learning_rate = java_edgewise_model_config.getLearningRate()
        self.weight_decay = java_edgewise_model_config.getWeightDecay()
        self.embedding_dim = java_edgewise_model_config.getEmbeddingDim()
        self.seed = java_edgewise_model_config.getSeed()
        self.conv_layer_configs = self.get_conv_layer_configs()
        self.vertex_input_property_names = java_edgewise_model_config.getVertexInputPropertyNames()
        self.vertex_input_property_names = java_edgewise_model_config.getVertexInputPropertyNames()
        if self.vertex_input_property_names:
            self.vertex_input_property_names = self.vertex_input_property_names.toArray()
        self.edge_input_property_names = java_edgewise_model_config.getEdgeInputPropertyNames()
        if self.edge_input_property_names:
            self.edge_input_property_names = self.edge_input_property_names.toArray()
        self.vertex_input_property_configs = self.get_vertex_input_property_configs()
        self.edge_input_property_configs = self.get_edge_input_property_configs()
        self.standardize = java_edgewise_model_config.isStandardize()
        self.normalize = java_edgewise_model_config.isNormalize()
        self.backend = conversion.enum_to_python_str(java_edgewise_model_config.getBackend())

    def get_conv_layer_configs(self) -> List[GraphWiseConvLayerConfig]:
        """Return a list of conv layer configs"""
        java_conv_layer_configs = java_handler(self._config.getConvLayerConfigs, [])
        conv_layer_configs = []
        for config in java_conv_layer_configs:
            params = {
                "weight_init_scheme": conversion.enum_to_python_str(config.getWeightInitScheme()),
                "activation_fn": conversion.enum_to_python_str(config.getActivationFunction()),
                "num_sampled_neighbors": config.getNumSampledNeighbors(),
                "neighbor_weight_property_name": config.getNeighborWeightPropertyName(),
                "dropout_rate": config.getDropoutRate(),
            }
            conv_layer_configs.append(GraphWiseConvLayerConfig(config, params))
        return conv_layer_configs

    def get_vertex_input_property_configs(self) -> Dict[str, InputPropertyConfig]:
        """Get the vertex input property configs."""
        java_vertex_input_property_configs = java_handler(
            self._config.getVertexInputPropertyConfigs, [])
        return _java_input_property_list_to_python_configs(
            java_vertex_input_property_configs
        )

    def get_edge_input_property_configs(self) -> Dict[str, InputPropertyConfig]:
        """Get the edge input property configs."""
        java_edge_input_property_configs = java_handler(
            self._config.getEdgeInputPropertyConfigs, [])
        print(java_edge_input_property_configs)
        return _java_input_property_list_to_python_configs(
            java_edge_input_property_configs
        )

    def set_batch_size(self, batch_size: int) -> None:
        """Set the batch size

        :param batch_size: batch size
        :type batch_size: int
        """
        java_handler(self._config.setBatchSize, [batch_size])
        self.batch_size = batch_size

    def set_num_epochs(self, num_epochs: int) -> None:
        """Set the number of epochs

        :param num_epochs: number of epochs
        :type num_epochs: int
        """
        java_handler(self._config.setNumEpochs, [num_epochs])
        self.num_epochs = num_epochs

    def set_learning_rate(self, learning_rate: float) -> None:
        """Set the learning rate

        :param learning_rate: initial learning rate
        :type learning_rate: int
        """
        java_handler(self._config.setLearningRate, [learning_rate])
        self.learning_rate = learning_rate

    def set_weight_decay(self, weight_decay: float) -> None:
        """Set the weight decay

        :param weight_decay: weight decay
        :type weight_decay: float
        """
        java_handler(self._config.setWeightDecay, [weight_decay])
        self.weight_decay = weight_decay

    def set_embedding_dim(self, embedding_dim: int) -> None:
        """Set the embedding dimension

        :param embedding_dim: embedding dimension
        :type embedding_dim: int
        """
        java_handler(self._config.setEmbeddingDim, [embedding_dim])
        self.embedding_dim = embedding_dim

    def set_seed(self, seed: int) -> None:
        """Set the seed

        :param seed: seed
        :type seed: int
        """
        java_handler(self._config.setSeed, [seed])
        self.seed = seed

    def set_fitted(self, fitted: bool) -> None:
        """Set the fitted flag

        :param fitted: fitted flag
        :type fitted: bool
        """
        java_handler(self._config.setFitted, [fitted])
        self.fitted = fitted

    def set_shuffle(self, shuffle: bool) -> None:
        """Set the shuffling flag

        :param shuffle: shuffling flag
        :type shuffle: bool
        """
        java_handler(self._config.setShuffle, [shuffle])
        self.shuffle = shuffle

    def set_training_loss(self, training_loss: float) -> None:
        """Set the training loss

        :param training_loss: training loss
        :type training_loss: float
        """
        java_handler(self._config.setTrainingLoss, [training_loss])
        self.training_loss = training_loss

    def set_input_feature_dim(self, input_feature_dim: int) -> None:
        """Set the input feature dimension

        :param input_feature_dim: input feature dimension
        :type input_feature_dim: int
        """
        java_handler(self._config.setInputFeatureDim, [input_feature_dim])
        self.input_feature_dim = input_feature_dim

    def set_edge_input_feature_dim(self, edge_input_feature_dim: int) -> None:
        """Set the edge input feature dimension

        :param edge_input_feature_dim: edge input feature dimension
        :type edge_input_feature_dim: int
        """
        java_handler(self._config.setEdgeInputFeatureDim, [edge_input_feature_dim])
        self.edge_input_feature_dim = edge_input_feature_dim

    def set_standardize(self, standardize: bool) -> None:
        """Set the standardize flag

        :param standardize: standardize flag
        :type standardize: bool
        """
        java_handler(self._config.setStandardize, [standardize])
        self.standardize = standardize

    def set_normalize(self, normalize: bool) -> None:
        """Whether or not normalization is enabled."""
        java_handler(self._config.setNormalize, [normalize])
        self.normalize = normalize
