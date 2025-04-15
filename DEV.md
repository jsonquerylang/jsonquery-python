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

To update requirements.txt, use https://azurda.github.io/

## Test

```bash
python -m unittest -v
```

## Format

```bash
ruff format
```

## Publish

1.  Format the code:

    ```
    ruff format
    ```

2.  Update the version number in `setup.py` using semantic versioning.

3.  Run the unit tests and check whether all tests pass:

    ```
    python -m unittest
    ```

4.  Commit and push the changes to GitHub.

5.  Add a version tag:

    ```
    git tag v1.2.3
    git push --tag
    ```

6.  Clear the `dist` folder

7.  Build the library:
 
    ```
    python -m build
    ```

8.  Publish on PyPi:

    ```
    twine check dist/*
    twine upload dist/*
    ```
