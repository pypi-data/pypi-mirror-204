# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:hydrogen
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Grid World example
#
# In this notebook we implement the GridWorld game with the
# `environment-framework` and use stable-baseliens3 to train a `DQN`-agent on it.


# %%
# pylint: disable=redefined-outer-name
import math
from random import randint
from typing import Any, Callable, Optional

import numpy as np
from gymnasium.spaces import Box, Discrete, Space
from numpy.typing import NDArray
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.dqn import DQN

from environment_framework import EnvironmentFrameworkGym, Level, PygameHumanVisualizer, Simulator

# %% [markdown]
# ## Implement the `Game`


# %%
class Action:
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3


class GridWorldGame:
    def __init__(self, size: int) -> None:
        self.size = size
        self.player_position = (0, 0)
        self.target_position = (0, 0)
        self.reset()

    @property
    def done(self) -> bool:
        return self.player_position == self.target_position

    @property
    def space(self) -> Space:
        return Discrete(4)

    def act(self, action: int, **_: Any) -> None:
        if action == Action.UP:
            self.player_position = (self.player_position[0], self.player_position[1] - 1)
        if action == Action.DOWN:
            self.player_position = (self.player_position[0], self.player_position[1] + 1)
        if action == Action.RIGHT:
            self.player_position = (self.player_position[0] + 1, self.player_position[1])
        if action == Action.LEFT:
            self.player_position = (self.player_position[0] - 1, self.player_position[1])
        corrected_x = max(0, min(self.size - 1, self.player_position[0]))
        corrected_y = max(0, min(self.size - 1, self.player_position[1]))
        self.player_position = (corrected_x, corrected_y)

    def reset(self) -> None:
        def get_random_position() -> int:
            return randint(0, self.size - 1)

        self.player_position = (get_random_position(), get_random_position())
        self.target_position = (get_random_position(), get_random_position())
        if self.done:
            self.reset()


# %% [markdown]
# ## Implement the `Observer` and the `Estimator`


# %%
class GridWorldObserver:
    def __init__(self, game: GridWorldGame) -> None:
        self.game = game

    @property
    def space(self) -> Space:
        return Box(shape=(4,), low=-math.inf, high=math.inf)

    def observe(self) -> NDArray:
        return np.array(
            [*self.game.player_position, *self.game.target_position],
            dtype=np.float32,
        )


class GridWorldEstimator:
    def __init__(self, game: GridWorldGame) -> None:
        self.game = game

    def estimate(self) -> float:
        return -1 + float(self.game.done)


# %% [markdown]
# ## Add a nice little `Visualizer`


# %%
class GridWorldVisualizer(PygameHumanVisualizer):
    BLUE = [0, 0, 255]
    GREEN = [0, 255, 0]

    def __init__(self, game: GridWorldGame) -> None:
        super().__init__(50)
        self.game = game

    def render_rgb(self) -> NDArray[np.uint8]:
        frame = [[[0 for k in range(3)] for j in range(self.game.size)] for i in range(self.game.size)]
        frame[self.game.player_position[1]][self.game.player_position[0]] = self.BLUE
        frame[self.game.target_position[1]][self.game.target_position[0]] = self.GREEN
        return np.array(frame, dtype=np.uint8)


# %% [markdown]
# ## Connect all together with a `Level`


# %%
class GridWorldLevel(Level):
    _game: GridWorldGame
    _observer: GridWorldObserver
    _estimator: GridWorldEstimator
    _visualizer: GridWorldVisualizer

    def reset(self) -> None:
        self._game.reset()

    def step(self, action: int) -> Any:
        self._game.act(action)


# %% [markdown]
# ## Look at a random selecting agent

# %%
game = GridWorldGame(7)
level = GridWorldLevel(
    game,
    GridWorldObserver(game),
    GridWorldEstimator(game),
    GridWorldVisualizer(game),
)
simulator = Simulator(level, 50)

FPS = 4
DONE = False
while not DONE:
    action = simulator.action_space.sample()
    simulator.step(action)
    obs = simulator.observe()
    reward = simulator.estimate()
    simulator.render_human(FPS)
    DONE = simulator.truncated or simulator.done
simulator.close()

# %% [markdown]
# ## Use stable-baselines3 to train an DQN-agent in the environment


# %%
def make_env(render_mode: Optional[str], rank: int, seed: int = 0, **_: Any) -> Callable:
    def _init() -> EnvironmentFrameworkGym:
        game = GridWorldGame(7)
        level = GridWorldLevel(
            game,
            GridWorldObserver(game),
            GridWorldEstimator(game),
            GridWorldVisualizer(game),
        )
        env = EnvironmentFrameworkGym(level, 10, render_mode=render_mode)
        env.reset(seed=seed + rank)
        return env

    set_random_seed(seed)
    return _init


# %%
N_CPU = 1
vec_env = SubprocVecEnv([make_env(None, i) for i in range(N_CPU)])
model = DQN("MlpPolicy", vec_env)
model.learn(
    total_timesteps=int(5e5),
    progress_bar=True,
)

# %%
model.save("gridworld-dqn.zip")

# %%
del model

# %%
game = GridWorldGame(7)
level = GridWorldLevel(game, GridWorldObserver(game), GridWorldEstimator(game), GridWorldVisualizer(game))
env = EnvironmentFrameworkGym(level, 10, render_mode="human")
model = DQN.load("gridworld-dqn.zip", env=env)
evaluate_policy(model, env, n_eval_episodes=10)
env.close()
