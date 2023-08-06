from typing import Any, Protocol

from gymnasium.spaces import Space


class Game(Protocol):
    @property
    def done(self) -> bool:
        """
        Indicates if the game has is done/finished.
        Sould be set if the end state is reached.

        Returns
        -------
        done : bool
            Game has reached its end state.
        """

    @property
    def space(self) -> Space:
        pass

    def act(self, action: Any, **kwargs: Any) -> None:
        """
        Implements the logic for a step in the game.

        Parameters
        ----------
        action : Any
            Action to act upon.
        """
