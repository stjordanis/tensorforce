# Copyright 2017 reinforce.io. All Rights Reserved.
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

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import tensorflow as tf

import unittest

from tensorforce import Configuration
from tensorforce.agents import DQNAgent
from tensorforce.core.networks import layered_network_builder
from tensorforce.environments.minimal_test import MinimalTest
from tensorforce.execution import Runner


class TestDQNAgent(unittest.TestCase):

    def test_discrete(self):
        environment = MinimalTest(continuous=False)
        config = Configuration(
            batch_size=8,
            learning_rate=0.001,
            memory_capacity=800,
            first_update=80,
            repeat_update=4,
            target_update_frequency=20,
            states=environment.states,
            actions=environment.actions
            # explorations=dict(
            #     name='epsilon_decay',
            #     args=(),
            #     kwargs=dict(
            #         epsilon=1,
            #         epsilon_final=0,
            #         epsilon_timesteps=50
            #     )
            # )
        )
        network_builder = layered_network_builder(layers_config=[{'type': 'dense', 'size': 32}])
        agent = DQNAgent(config=config, network_builder=network_builder)
        runner = Runner(agent=agent, environment=environment)

        def episode_finished(r):
            return r.episode < 100 or not all(x >= 1.0 for x in r.episode_rewards[-100:])

        runner.run(episodes=1000, episode_finished=episode_finished)
        self.assertTrue(runner.episode < 1000)