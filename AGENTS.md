# Agents Knowledge

## Code Conventions

- Write modular, clean and fully typed modern python code.
- Prefer logger instead of print statements.
- Log lines and exceptions should always start with a lowercase char.
- Use python 3.11+ style typing.
- Try not to use `Any` for typing.


## Linting
```
make lint
```

```
make mypy
```

## Formatting


```
make format
```

## Dependency Management

We use uv to manage Python dependencies.

Run

```
uv add <your-package-name>
```

This installs the package and adds it to `pyproject.toml`.
