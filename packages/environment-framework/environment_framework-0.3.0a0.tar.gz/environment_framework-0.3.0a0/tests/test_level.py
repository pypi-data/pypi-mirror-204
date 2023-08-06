from unittest.mock import MagicMock

import pytest
from gymnasium.spaces import Discrete, Space

from environment_framework.estimator import Estimator
from environment_framework.game import Game
from environment_framework.level import Level
from environment_framework.observer import Observer
from environment_framework.visualizer import Visualizer


@pytest.fixture
def setup() -> Level:
    class LevelImpl(Level):
        @property
        def observation_space(self) -> Space:
            return Discrete(1)

        @property
        def action_space(self) -> Space:
            return Discrete(10)

        def step(self, action: int) -> None:
            assert True

        def reset(self) -> None:
            assert True

    game = MagicMock(spec_set=Game)
    observer = MagicMock(spec_set=Observer)
    estimator = MagicMock(spec_set=Estimator)
    visualizer = MagicMock(spec_set=Visualizer)

    return LevelImpl(game, observer, estimator, visualizer)


def test_done(setup: Level) -> None:
    level = setup
    level._game.done = True
    assert level.done
    level._game.done = False
    assert not level.done


def test_observe(setup: Level) -> None:
    level = setup
    level.observe()

    level._observer.observe.assert_called_once()


def test_estimate(setup: Level) -> None:
    level = setup
    level.estimate()

    level._estimator.estimate.assert_called_once()


def test_render(setup: Level) -> None:
    level = setup
    level.render_rgb()

    level._visualizer.render_rgb.assert_called_once()
