PROJECT_NAME = watching-the-clouds
REGION = eu-west-2
PYTHON_INTERPRETER = python3
PYTHONPATH:=$(shell pwd)/src/transform:$(shell pwd)/src/extract:$(shell pwd)/src/load
SHELL := /bin/bash
PROFILE = default
PIP:=pip

create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)

ACTIVATE_ENV := source venv/bin/activate

define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

requirements: create-environment
	$(call execute_in_env, $(PIP) install pip-tools)
	$(call execute_in_env, pip-compile requirements.in)
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)
	
## SETUP
bandit:
	$(call execute_in_env, $(PIP) install bandit)

black:
	$(call execute_in_env, $(PIP) install black)

coverage:
	$(call execute_in_env, $(PIP) install coverage)

dev-setup: bandit black coverage

## RUN
security-test:
	$(call execute_in_env, bandit -lll */*/*.py *c/*/*.py)

run-black:
	$(call execute_in_env, black  ./src/*/*.py ./test/*/*.py)

unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest -v)

check-coverage:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest --cov=src test/)

run-checks: security-test run-black unit-test check-coverage