from typing import Protocol

import numpy as np
from numpy.typing import NDArray


class Visualizer(Protocol):
    def render_rgb(self) -> NDArray[np.uint8]:
        """
        Renders the given visualizee to a visualisation.

        Parameters
        ----------
        visualizee: Any
            Object to visualise.

        Returns
        -------
        visualisation: Any
            The visualisation of the object.
        """

    def render_human(self, fps: int) -> None:
        pass

    def close(self) -> None:
        pass
