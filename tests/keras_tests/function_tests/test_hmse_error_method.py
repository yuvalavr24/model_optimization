# Copyright 2024 Sony Semiconductor Israel, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import unittest

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

import model_compression_toolkit as mct
from model_compression_toolkit import DefaultDict
from model_compression_toolkit.core import QuantizationConfig
from model_compression_toolkit.constants import THRESHOLD, RANGE_MAX, NUM_QPARAM_HESSIAN_SAMPLES
from model_compression_toolkit.core.common.hessian import HessianInfoService, HessianScoresRequest, HessianMode, \
    HessianScoresGranularity
from model_compression_toolkit.core.common.model_collector import ModelCollector
from model_compression_toolkit.core.common.quantization.quantization_params_generation.qparams_computation import \
    calculate_quantization_params
from model_compression_toolkit.core.keras.constants import KERNEL, GAMMA
from model_compression_toolkit.target_platform_capabilities.constants import KERNEL_ATTR, BIAS_ATTR, KERAS_KERNEL, BIAS
from model_compression_toolkit.target_platform_capabilities.target_platform import AttributeQuantizationConfig
from model_compression_toolkit.target_platform_capabilities.tpc_models.imx500_tpc.latest import generate_keras_tpc
from model_compression_toolkit.core.keras.default_framework_info import DEFAULT_KERAS_INFO
from model_compression_toolkit.core.keras.keras_implementation import KerasImplementation
from model_compression_toolkit.target_platform_capabilities.tpc_models.imx500_tpc.latest import \
    get_op_quantization_configs
from tests.common_tests.helpers.generate_test_tp_model import generate_test_tp_model
from tests.common_tests.helpers.prep_graph_for_func_test import prepare_graph_with_configs

tp = mct.target_platform


def model_gen():
    inputs = layers.Input(shape=[8, 8, 3])
    x = layers.Conv2D(2, 3, padding='same')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Activation('relu')(x)
    x = layers.Dense(8)(x)
    return tf.keras.models.Model(inputs=inputs, outputs=x)


def no_bn_fusion_model_gen():
    inputs = layers.Input(shape=[8, 8, 3])
    x = layers.Conv2D(2, 3, padding='same')(inputs)
    x = layers.Activation('relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation('relu')(x)
    x = layers.Dense(8)(x)
    return tf.keras.models.Model(inputs=inputs, outputs=x)


def representative_dataset():
    yield [np.random.randn(1, 8, 8, 3).astype(np.float32)]


def get_tpc(quant_method, per_channel):
    tp = generate_test_tp_model(edit_params_dict={
        'weights_quantization_method': quant_method,
        'weights_per_channel_threshold': per_channel})
    tpc = generate_keras_tpc(name="hmse_params_selection_test", tp_model=tp)

    return tpc


class TestParamSelectionWithHMSE(unittest.TestCase):
    def _setup_with_args(self, quant_method, per_channel, running_gptq=True, tpc_fn=get_tpc, model_gen_fn=model_gen):
        self.qc = QuantizationConfig(weights_error_method=mct.core.QuantizationErrorMethod.HMSE)
        self.float_model = model_gen_fn()
        self.keras_impl = KerasImplementation()
        self.fw_info = DEFAULT_KERAS_INFO
        self.quant_method = quant_method
        self.per_channel = per_channel

        self.graph = prepare_graph_with_configs(self.float_model, self.keras_impl, self.fw_info,
                                                representative_dataset,
                                                lambda name, _tp: tpc_fn(quant_method, per_channel),
                                                qc=self.qc,
                                                running_gptq=running_gptq  # to enable HMSE in params calculation if needed
                                                )

        self.his = HessianInfoService(graph=self.graph, fw_impl=self.keras_impl)

        mi = ModelCollector(self.graph,
                            fw_impl=self.keras_impl,
                            fw_info=self.fw_info,
                            qc=self.qc)

        for i in range(10):
            mi.infer([np.random.randn(1, 8, 8, 3)])

    def _verify_params_calculation_execution(self, param_name):
        def _run_node_verification(node_type):
            node = [n for n in self.graph.nodes if n.type == node_type]
            self.assertTrue(len(node) == 1, f"Expecting exactly 1 {node_type} node in test model.")
            node = node[0]

            kernel_attr_qparams = (
                node.candidates_quantization_cfg[0].weights_quantization_cfg.get_attr_config(KERNEL))
            self.assertTrue(kernel_attr_qparams.weights_quantization_params.get(param_name) is not None,
                            f"Expecting {node_type} node parameters {param_name} to be initialized.")
            expected_hessian_request = HessianScoresRequest(mode=HessianMode.WEIGHTS,
                                                            granularity=HessianScoresGranularity.PER_ELEMENT,
                                                            data_loader=None,
                                                            n_samples=1,
                                                            target_nodes=[node])
            # check hessians have been precomputed (dataloader=None fetches from cache)
            hess = self.his.fetch_hessian(expected_hessian_request)
            self.assertTrue(hess[node.name].shape[0] == 1), ('Expected 1 hessian to be fetched from cache '
                                                             '(with None dataloader)')

        _run_node_verification(layers.Conv2D)
        _run_node_verification(layers.Dense)

    def test_pot_threshold_selection_hmse_per_channel(self):

        self._setup_with_args(quant_method=mct.target_platform.QuantizationMethod.POWER_OF_TWO, per_channel=True)
        calculate_quantization_params(self.graph, fw_impl=self.keras_impl, repr_data_gen_fn=representative_dataset,
                                      hessian_info_service=self.his, num_hessian_samples=1)
        self._verify_params_calculation_execution(THRESHOLD)

    def test_pot_threshold_selection_hmse_per_tensor(self):

        self._setup_with_args(quant_method=mct.target_platform.QuantizationMethod.POWER_OF_TWO, per_channel=False)
        calculate_quantization_params(self.graph, fw_impl=self.keras_impl, repr_data_gen_fn=representative_dataset,
                                      hessian_info_service=self.his, num_hessian_samples=1)
        self._verify_params_calculation_execution(THRESHOLD)

    def test_symmetric_threshold_selection_hmse_per_channel(self):

        self._setup_with_args(quant_method=mct.target_platform.QuantizationMethod.SYMMETRIC, per_channel=True)
        calculate_quantization_params(self.graph, fw_impl=self.keras_impl, repr_data_gen_fn=representative_dataset,
                                      hessian_info_service=self.his, num_hessian_samples=1)
        self._verify_params_calculation_execution(THRESHOLD)

    def test_symmetric_threshold_selection_hmse_per_tensor(self):

        self._setup_with_args(quant_method=mct.target_platform.QuantizationMethod.SYMMETRIC, per_channel=False)
        calculate_quantization_params(self.graph, fw_impl=self.keras_impl, repr_data_gen_fn=representative_dataset,
                                      hessian_info_service=self.his, num_hessian_samples=1)
        self._verify_params_calculation_execution(THRESHOLD)

    def test_usniform_threshold_selection_hmse_per_channel(self):

        self._setup_with_args(quant_method=mct.target_platform.QuantizationMethod.UNIFORM, per_channel=True)
        calculate_quantization_params(self.graph, fw_impl=self.keras_impl, repr_data_gen_fn=representative_dataset,
                                      hessian_info_service=self.his, num_hessian_samples=1)
        self._verify_params_calculation_execution(RANGE_MAX)

    def test_uniform_threshold_selection_hmse_per_tensor(self):

        self._setup_with_args(quant_method=mct.target_platform.QuantizationMethod.UNIFORM, per_channel=False)
        calculate_quantization_params(self.graph, fw_impl=self.keras_impl, repr_data_gen_fn=representative_dataset,
                                      hessian_info_service=self.his, num_hessian_samples=1)
        self._verify_params_calculation_execution(RANGE_MAX)

    def test_threshold_selection_hmse_no_gptq(self):
        with self.assertRaises(ValueError) as e:
            self._setup_with_args(quant_method=mct.target_platform.QuantizationMethod.SYMMETRIC, per_channel=True,
                                  running_gptq=False)
        self.assertTrue('The HMSE error method for parameters selection is only supported when running GPTQ '
                        'optimization due to long execution time that is not suitable for basic PTQ.' in e.exception.args[0])

    def test_threshold_selection_hmse_no_kernel_attr(self):
        def _generate_bn_quantization_tpc(quant_method, per_channel):
            cfg, _, _ = get_op_quantization_configs()
            conv_qco = tp.QuantizationConfigOptions([cfg], base_config=cfg)

            # enable BN attributes quantization using the
            bn_qco = conv_qco.clone_and_edit(attr_weights_configs_mapping=
                                             {GAMMA: AttributeQuantizationConfig(weights_n_bits=8,
                                                                                 enable_weights_quantization=True)})

            tp_model = tp.TargetPlatformModel(conv_qco)

            with tp_model:
                tp.OperatorsSet("Linear", conv_qco)
                tp.OperatorsSet("BN", bn_qco)

            tpc = tp.TargetPlatformCapabilities(tp_model)

            with tpc:
                tp.OperationsSetToLayers(
                    "Linear",
                    [layers.Conv2D, layers.Dense],
                    attr_mapping={KERNEL_ATTR: DefaultDict(default_value=KERAS_KERNEL),
                                  BIAS_ATTR: DefaultDict(default_value=BIAS)}
                )

                tp.OperationsSetToLayers(
                    "BN",
                    [layers.BatchNormalization],
                    attr_mapping={GAMMA: DefaultDict(default_value=GAMMA)}
                )

            return tpc

        self._setup_with_args(quant_method=mct.target_platform.QuantizationMethod.SYMMETRIC, per_channel=True,
                              tpc_fn=_generate_bn_quantization_tpc, model_gen_fn=no_bn_fusion_model_gen)
        calculate_quantization_params(self.graph, fw_impl=self.keras_impl, repr_data_gen_fn=representative_dataset,
                                      hessian_info_service=self.his, num_hessian_samples=1)

        # Verify Conv and Dense layers used HMSE
        self._verify_params_calculation_execution(THRESHOLD)

        # Verify BN used default MSE (didn't compute Hessian)
        node_type = layers.BatchNormalization
        node = [n for n in self.graph.nodes if n.type == node_type]
        self.assertTrue(len(node) == 1, f"Expecting exactly 1 {node_type} node in test model.")
        node = node[0]

        expected_hessian_request = HessianScoresRequest(mode=HessianMode.WEIGHTS,
                                                        granularity=HessianScoresGranularity.PER_ELEMENT,
                                                        data_loader=None,
                                                        n_samples=1,
                                                        target_nodes=[node])

        with self.assertRaises(ValueError) as e:
            self.his.fetch_hessian(expected_hessian_request)
        self.assertTrue('Not enough hessians are cached to fulfill the request' in e.exception.args[0])


if __name__ == '__main__':
    unittest.main()
