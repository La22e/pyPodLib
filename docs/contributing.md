# Contributing

Contributions are welcome! Please open an issue or pull request on [GitHub](https://github.com/TheRealSavi/pyPodLib).

## Local development

```console
git clone https://github.com/TheRealSavi/pyPodLib.git
cd pyPodLib
pip install -e '.[dev]'
```

## Running tests

```console
pytest -v
```

## Code style

```console
ruff check .
```

The project follows [Ruff](https://docs.astral.sh/ruff/) conventions and the standard Python type hinting style. All contributions should pass `ruff check` and all tests before merging.
