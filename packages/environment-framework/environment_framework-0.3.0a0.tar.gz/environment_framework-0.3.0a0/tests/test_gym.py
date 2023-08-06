from typing import List, Tuple
from unittest.mock import MagicMock
from typing import Any

import numpy as np
from numpy.typing import NDArray
import pytest

from gymnasium.spaces import Discrete, Space

from environment_framework.estimator import Estimator
from environment_framework.game import Game
from environment_framework.gym import EnvironmentFrameworkGym
from environment_framework.level import Level
from environment_framework.ilevel import ILevel
from environment_framework.observer import Observer
from environment_framework.simulator import Simulator
from environment_framework.visualizer import Visualizer


class TestLevel(Level):
    __test__ = False

    @property
    def done(self) -> bool:
        return True

    @property
    def observation_space(self) -> Space:
        return Discrete(
            10,
        )

    @property
    def action_space(self) -> Space:
        return Discrete(10)

    def reset(self) -> None:
        ...

    def step(self, action: int) -> bool:
        return True

    def observe(self) -> NDArray:
        return np.zeros((10,))


class TestSimulation:
    __test__ = False

    def __init__(self, level: Level, settings: int) -> None:
        self.level = level
        self.level_settings = settings


SetupT = Tuple[EnvironmentFrameworkGym, MagicMock]


@pytest.fixture
def setup() -> SetupT:
    game_mock = MagicMock(spec_set=Game)
    observer_mock = MagicMock(spec_set=Observer)
    estimator_mock = MagicMock(spec_set=Estimator)
    visualizer_mock = MagicMock(spec_set=Visualizer)

    level: ILevel = TestLevel(game_mock, observer_mock, estimator_mock, visualizer_mock)
    simulator_mock = MagicMock(spec_set=Simulator)
    gym = EnvironmentFrameworkGym(level, 100, render_mode="rgb_array")
    gym.simulator = simulator_mock
    return gym, simulator_mock


def test_step(setup: SetupT) -> None:
    gym, simulator_mock = setup

    simulator_mock.estimate.return_value = 42
    simulator_mock.observe.return_value = np.array([42])
    simulator_mock.done = True
    simulator_mock.truncated = False

    observation, reward, done, truncated, extra = gym.step([10])

    assert observation == np.array([42])
    assert reward == 42
    assert truncated == False
    assert done
    assert extra == {}


def test_reset(setup: SetupT) -> None:
    gym, simulator_mock = setup

    simulator_mock.observe.return_value = [42]
    observation = gym.reset()

    simulator_mock.reset.assert_called_once()
    assert observation == ([42], {})


def test_render(setup: SetupT) -> None:
    gym, simulator_mock = setup
    simulator_mock.render_rgb.return_value = "frame"
    frame = gym.render()

    simulator_mock.render_rgb.assert_called_once()
    assert frame == "frame"
