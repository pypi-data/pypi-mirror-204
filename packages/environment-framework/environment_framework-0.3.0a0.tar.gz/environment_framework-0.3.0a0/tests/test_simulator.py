from unittest.mock import MagicMock, PropertyMock

import pytest

from environment_framework.level import Level
from environment_framework.simulator import Simulator


@pytest.fixture
def setup() -> Simulator:
    simulation_mock = MagicMock()
    level_mock = MagicMock(spec_set=Level)

    return Simulator(level_mock, 10000)


def test_action_space(setup: Simulator) -> None:
    simulator = setup
    simulator.level.action_space = "Testee"

    assert simulator.action_space == "Testee"


def test_observation_space(setup: Simulator) -> None:
    simulator = setup
    simulator.level.observation_space = "Testee"

    assert simulator.observation_space == "Testee"


def test_done(setup: Simulator) -> None:
    simulator = setup

    simulator.level.done = False
    assert not simulator.done

    simulator.level.done = True
    assert simulator.done

    simulator.level.done = False
    simulator.current_episodes_steps_done = 9999
    assert not simulator.truncated

    simulator.current_episodes_steps_done = 10000
    assert simulator.truncated


def test_clear_counter(setup: Simulator) -> None:
    simulator = setup
    simulator.current_episodes_steps_done = 1000

    simulator.clear_counter()

    assert simulator.current_episodes_steps_done == 0


def test_reset(setup: Simulator) -> None:
    simulator = setup
    simulator.current_episodes_steps_done = 100
    simulator.reset()

    simulator.level.reset.assert_called_once()
    assert simulator.current_episodes_steps_done == 0


def test_step(setup: Simulator) -> None:
    simulator = setup
    simulator.step(10)

    simulator.level.step.assert_called_once_with(10)
    assert simulator.current_episodes_steps_done == 1


def test_observe(setup: Simulator) -> None:
    simulator = setup
    simulator.observe()
    simulator.level.observe.assert_called_once()


def test_estimate(setup: Simulator) -> None:
    simulator = setup
    simulator.estimate()
    simulator.level.estimate.assert_called_once()


def test_render(setup: Simulator) -> None:
    simulator = setup
    simulator.render_rgb()
    simulator.level.render_rgb.assert_called_once()
