from abc import ABC, abstractmethod
from typing import Any

from gymnasium.spaces import Space
from numpy.typing import NDArray

from environment_framework.estimator import Estimator
from environment_framework.game import Game
from environment_framework.observer import Observer
from environment_framework.visualizer import Visualizer


class Level(ABC):
    """
    Manages the lifecycle of a game and its observer and estimator.
    Is used within the Simulator to step through a Simulation.
    """

    def __init__(
        self,
        game: Game,
        observer: Observer,
        estimator: Estimator,
        visualizer: Visualizer,
    ) -> None:
        """
        Parameters
        ----------
            game: Game
                The game in which the level takes place.
            observer: Observer
                The observer of the game.
            estimator: Estimator
                The estimator of the game.
            visualizer: Visualizer
                The visualizer of the game.
        """
        self._game = game
        self._observer = observer
        self._estimator = estimator
        self._visualizer = visualizer

    @property
    def done(self) -> bool:
        """
        Returns if the game in the level has reached the end state.

        Returns
        -------
            done: bool
                Game has reached its end state.
        """
        return self._game.done

    @property
    def observation_space(self) -> Space:
        """
        Return the desciribtion of the observation space.

        Returns
        -------
            observation_space: ObservationSpace
                The observation space describtion.
        """
        return self._observer.space

    @property
    def action_space(self) -> Space:
        """
        Return the desciribtion of the action space.

        Returns
        -------
            observation_space: ActionSpace
                The action space describtion.
        """
        return self._game.space

    @abstractmethod
    def reset(self) -> None:
        """
        Reset the level.
        """

    @abstractmethod
    def step(self, action: Any) -> Any:
        """
        Take a step in the level with a given action.

        Parameters
        ----------
            action: Any
                Object which describes the action.
        Returns
        -------
            state: Any
                The step in which is the level after the action.
        """

    def observe(self) -> NDArray:
        """
        Observes the level and returns an observation.

        Returns
        -------
            observation: List[float]
                Observation of the current level state.
        """
        return self._observer.observe()

    def estimate(self) -> float:
        """
        Estimates the level state and returns a estimation value.

        Returns
        -------
            estimation: float
                Estimated reward of the current level state.
        """
        return self._estimator.estimate()

    def render_rgb(self) -> Any:
        """
        Renders the current level state into a visualisation.

        Returns
        -------
            visualisation: Any
                Rendered visualisation of the current level state.
        """
        return self._visualizer.render_rgb()

    def render_human(self, fps: int) -> Any:
        return self._visualizer.render_human(fps)

    def close(self) -> Any:
        self._visualizer.close()
