# Copyright 2019 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Genetic-Attack test.
"""
import gc
import numpy as np
import pytest

import mindspore.ops.operations as M
from mindspore import Tensor
from mindspore import context
from mindspore.nn import Cell

from mindarmour import BlackModel
from mindarmour.adv_robustness.attacks import GeneticAttack


# for user
class ModelToBeAttacked(BlackModel):
    """model to be attack"""

    def __init__(self, network):
        super(ModelToBeAttacked, self).__init__()
        self._network = network

    def predict(self, inputs):
        """predict"""
        result = self._network(Tensor(inputs.astype(np.float32)))
        return result.asnumpy()


class DetectionModel(BlackModel):
    """model to be attack"""

    def predict(self, inputs):
        """predict"""
        # Adapt to the input shape requirements of the target network if inputs is only one image.
        if len(inputs.shape) == 3:
            inputs_num = 1
        else:
            inputs_num = inputs.shape[0]
        box_and_confi = []
        pred_labels = []
        gt_number = np.random.randint(1, 128)

        for _ in range(inputs_num):
            boxes_i = np.random.random((gt_number, 5))
            labels_i = np.random.randint(0, 10, gt_number)
            box_and_confi.append(boxes_i)
            pred_labels.append(labels_i)
        return np.array(box_and_confi), np.array(pred_labels)


class SimpleNet(Cell):
    """
    Construct the network of target model.

    Examples:
        >>> net = SimpleNet()
    """

    def __init__(self):
        """
        Introduce the layers used for network construction.
        """
        super(SimpleNet, self).__init__()
        self._softmax = M.Softmax()

    def construct(self, inputs):
        """
        Construct network.

        Args:
            inputs (Tensor): Input data.
        """
        out = self._softmax(inputs)
        return out


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_genetic_attack():
    """
    Genetic_Attack test
    """
    context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")
    batch_size = 6

    net = SimpleNet()
    inputs = np.random.rand(batch_size, 10)

    model = ModelToBeAttacked(net)
    labels = np.random.randint(low=0, high=10, size=batch_size)
    labels = np.eye(10)[labels]
    labels = labels.astype(np.float32)

    attack = GeneticAttack(model, pop_size=6, mutation_rate=0.05,
                           per_bounds=0.1, step_size=0.25, temp=0.1,
                           sparse=False)
    _, adv_data, _ = attack.generate(inputs, labels)
    assert np.any(inputs != adv_data)
    del inputs, labels, adv_data
    gc.collect()

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_supplement():
    context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")
    batch_size = 6

    net = SimpleNet()
    inputs = np.random.rand(batch_size, 10)

    model = ModelToBeAttacked(net)
    labels = np.random.randint(low=0, high=10, size=batch_size)
    labels = np.eye(10)[labels]
    labels = labels.astype(np.float32)

    attack = GeneticAttack(model, pop_size=6, mutation_rate=0.05,
                           per_bounds=0.1, step_size=0.25, temp=0.1,
                           adaptive=True,
                           sparse=False)
    # raise error
    _, _, _ = attack.generate(inputs, labels)
    del inputs, labels
    gc.collect()

@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_value_error():
    """test that exception is raised for invalid labels"""
    context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")
    batch_size = 6

    net = SimpleNet()
    inputs = np.random.rand(batch_size, 10)

    model = ModelToBeAttacked(net)
    labels = np.random.randint(low=0, high=10, size=batch_size)
    # labels = np.eye(10)[labels]
    labels = labels.astype(np.float32)

    attack = GeneticAttack(model, pop_size=6, mutation_rate=0.05,
                           per_bounds=0.1, step_size=0.25, temp=0.1,
                           adaptive=True,
                           sparse=False)
    # raise error
    with pytest.raises(ValueError):
        assert attack.generate(inputs, labels)
    del inputs, labels
    gc.collect()

@pytest.mark.level0
@pytest.mark.platform_x86_cpu
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_genetic_attack_detection_cpu():
    """
    Genetic_Attack test
    """
    context.set_context(mode=context.GRAPH_MODE, device_target="CPU")
    batch_size = 2
    inputs = np.random.random((batch_size, 100, 100, 3))
    model = DetectionModel()
    attack = GeneticAttack(model, model_type='detection', pop_size=6, mutation_rate=0.05,
                           per_bounds=0.1, step_size=0.25, temp=0.1,
                           sparse=False, max_steps=50)

    # generate adversarial samples
    adv_imgs = []
    for i in range(batch_size):
        img_data = np.expand_dims(inputs[i], axis=0)
        pre_gt_boxes, pre_gt_labels = model.predict(inputs)
        _, adv_img, _ = attack.generate(img_data, (pre_gt_boxes, pre_gt_labels))
        adv_imgs.append(adv_img)
    assert np.any(inputs != np.array(adv_imgs))
    del inputs, adv_imgs
    gc.collect()
