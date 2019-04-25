# ardtest

To run tests, you have to run virtual environment for this repository.

### Running venv

Set python version for repo and set venv and activate.
```sh
$ pyenv local 3.7.2
$ python -m venv env
$ source env/bin/activate
```

### Install python dependencies in repo directory
```sh
pip install -U setuptools pip
pip install -e .
```

### Run tests
```sh
$ pytest -sv
```

models - directory with tasks source code

tests - directory with tests

tmp - directory prepared for csv files