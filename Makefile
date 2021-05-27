PYTHON ?= python
TESTRUNNER ?= tox
TESTRUNNERFLAGS ?= -v tests
LINT := flake8
LINTFLAGS := jump

all: build

build: _jump.so

_jump.so: jump/jump.c
	$(PYTHON) setup.py build_ext --inplace

.PHONY: test
test:
	$(TESTRUNNER) $(TESTRUNNERFLAGS)

.PHONY: lint
lint:
	$(LINT) $(LINTFLAGS)

.PHONY: clean
clean:
	$(RM) _jump*.so
	$(RM) -r build dist *.egg-info docs/_build .tox .mypy_cache .pytest_cache
	find . -name "*.py[co]" -delete
	find . -name __pycache__ | xargs rm -rf
