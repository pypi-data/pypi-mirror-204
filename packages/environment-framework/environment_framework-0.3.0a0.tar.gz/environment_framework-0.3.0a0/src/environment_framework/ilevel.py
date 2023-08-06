from typing import Any, Protocol

from gymnasium.spaces import Space
from numpy.typing import NDArray


class ILevel(Protocol):
    @property
    def done(self) -> bool:
        """
        Returns if the game in the level has reached the end state.

        Returns
        -------
            done: bool
                Game has reached its end state.
        """

    @property
    def observation_space(self) -> Space:
        """
        Return the desciribtion of the observation space.

        Returns
        -------
            observation_space: ObservationSpace
                The observation space describtion.
        """

    @property
    def action_space(self) -> Space:
        """
        Return the desciribtion of the action space.

        Returns
        -------
            observation_space: ActionSpace
                The action space describtion.
        """

    def reset(self) -> None:
        """
        Reset the level.
        """

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

    def estimate(self) -> float:
        """
        Estimates the level state and returns a estimation value.

        Returns
        -------
            estimation: float
                Estimated reward of the current level state.
        """

    def render_rgb(self) -> Any:
        """
        Renders the current level state into a visualisation.

        Returns
        -------
            visualisation: Any
                Rendered visualisation of the current level state.
        """

    def render_human(self, fps: int) -> Any:
        pass

    def close(self) -> Any:
        pass
