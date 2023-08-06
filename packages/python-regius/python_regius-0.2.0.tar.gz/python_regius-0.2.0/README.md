# Python Regius

A simple & friendly Python RPC framework.

## Install

```bash
pip install python-regius
```

## Server Usage

Write a file named `__init__.py` in current directory.

```python
def add(a, b):
    return a + b
```

And Run

```bash
sanic regius:app
```

## Client Usage

```python
from regius import add

print(add(1, 2))
```
