# Development

## install

Create, activate, deactivate a virtual environment:

```bash
python -m venv venv

.\venv\Scripts\activate

deactivate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Test

```bash
python -m unittest -v
```

## Format

```bash
ruff format
```

## Publish

```
python .\setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
```
