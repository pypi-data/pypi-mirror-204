![License](https://img.shields.io/github/license/crzdg/environment-framework)
![Last Commit](https://img.shields.io/github/last-commit/crzdg/environment-framework)
![Coverage](https://raw.githubusercontent.com/gist/crzdg/e60a9d0af9c141f6d2a3e0bd09366f5f/raw/coverage-badge.svg)
![Tests](https://raw.githubusercontent.com/gist/crzdg/79f221f23ccd460bba50b81f0df78ae1/raw/tests-badge.svg)
![PyPI](https://img.shields.io/pypi/pyversions/environment-framework)
![PyPI](https://img.shields.io/pypi/status/environment-framework)
![PyPI](https://img.shields.io/pypi/v/environment-framework)


# 🌐 Environment Framework

This repository contains the Python package `environment-framework`. The project aims to provide loose building blocks to manage the logic, observation, estimation and visualization of an agent-environment loop. It can be used to implement problems which might be solved with reinforcement learning or dynamic programming algorithms.

A wrapper around [`gymnasium`](https://github.com/Farama-Foundation/Gymnasium) is provided to connect to well-known frameworks in the field.

> The wrapper for gymnasium uses the gymnasium>=0.26 API structure!

### 🤔 Why create this project?

The project emerges from a previous project of mine. It was used to separate the different elements of the projects agent-environment-loop. 

## 🚀 Get Started

#### Installation

```bash
pip3 install environment-framework
```

### 👩‍🏫 GridWorld Example

The implemented example of `GridWorld` can also be found in a Jupyter notebook [grid_world.ipynb](example/grid_world.ipynb).

```bash
pip3 install "environment-framework[extra]"
jupyter lab
```

```python
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

class GridWorldLevel(Level):
    _game: GridWorldGame
    _observer: GridWorldObserver
    _estimator: GridWorldEstimator
    _visualizer: GridWorldVisualizer

    def reset(self) -> None:
        self._game.reset()

    def step(self, action: int) -> Any:
        self._game.act(action)

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
```

### 📃 Documentation

Some doc-strings are already added. Documentation is a work-in-progress and will be updated on a time by time basis.

### 💃🕺 Contribution

I welcome everybody contributing to this project. Please read the [CONTRIBUTING.md](./CONTRIBUTING.md) for more information.
Feel free to open an issue on the project if you have any further questions.

## 💻 Development

The repository provides tools for development using [hatch](https://hatch.pypa.io/latest/).

All dependencies for the project also can be found in a `requirements`-file.

Install the development dependencies.

```bash
pip3 install -r requirements/dev.txt
```

or 

```bash
pip3 install "environment-framework[dev]"
```

#### Tools

To run all development tools, type checking, linting and tests `hatch` is required.

```bash
make all
```

#### Type checking

Type checking with `mypy`.

```bash
make mypy
```

#### Linting

Linting with `pylint`.

```bash
make lint
```

#### Tests

Run tests with `pytest`.

```bash
make test
```

#### Update dependencies

Update python requirements with `pip-compile`.

```bash
make update
```

## 🧾 License

This repository is licensed under the MIT License.
