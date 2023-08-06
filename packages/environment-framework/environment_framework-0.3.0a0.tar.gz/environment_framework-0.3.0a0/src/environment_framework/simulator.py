from typing import Any

from gymnasium.spaces import Space
from numpy.typing import NDArray

from environment_framework.ilevel import ILevel


class Simulator:  # pylint: disable = too-many-instance-attributes
    """
    Runs simulations on a Level.
    """

    # TODO: Add a proper state which is passed to the observe,estimate and render method.
    def __init__(self, level: ILevel, max_episode_steps: int) -> None:
        self.level = level
        self._max_episode_steps = max_episode_steps
        self.current_episodes_steps_done = 0

    @property
    def action_space(self) -> Space:
        return self.level.action_space

    @property
    def observation_space(self) -> Space:
        return self.level.observation_space

    @property
    def done(self) -> bool:
        """
        If the current simulation is finished.

        Returns
        -------
            done: bool
                Simulator is finished.
        """
        return self.level.done

    @property
    def truncated(self) -> bool:
        return self.current_episodes_steps_done >= self._max_episode_steps

    def clear_counter(self) -> None:
        """
        Clear the counters of the Simulator.
        """
        self.current_episodes_steps_done = 0

    def reset(self) -> None:
        """
        Reset the Level and prepare for a new simulation.
        """
        self.level.reset()
        self.current_episodes_steps_done = 0

    def step(self, action: Any) -> Any:
        """
        Take a step in the Simulator through performing an action in the Level.

        Parameters
        ----------
            action: Any
                Action to take in the level.

        Returns
        -------
            taken_action: Any
                Returns the action taken in the Level.
        """
        self.current_episodes_steps_done += 1
        return self.level.step(action)

    def observe(self) -> NDArray:
        """
        Observes the level and returns an observation.

        Returns
        -------
            observation: List[float]
                Observation of the current level state.
        """
        return self.level.observe()

    def estimate(self) -> float:
        """
        Estimates the level state and returns a estimation value.

        Returns
        -------
            estimation: float
                Estimated reward of the current level state.
        """
        return self.level.estimate()

    def render_rgb(self) -> Any:
        """
        Renders the current level state into a visualisation.

        Returns
        -------
            visualisation: Any
                Rendered visualisation of the current level state.
        """
        return self.level.render_rgb()

    def render_human(self, fps: int) -> None:
        self.level.render_human(fps)

    def close(self) -> None:
        self.level.close()
