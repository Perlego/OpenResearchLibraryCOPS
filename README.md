# OpenResearchLibraryCOPS

# run tests:
`pipenv shell`
(first time only) `pipenv install`
`cp config_example.py config.py`
and fill in your credentials to config.py
`export PYTHONPATH=$PYTHONPATH:$PWD/src`
`pipenv run python -m pytest tests/`
