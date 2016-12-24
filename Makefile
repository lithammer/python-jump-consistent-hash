PYTHON ?= python
TESTRUNNER ?= py.test
TESTRUNNERFLAGS ?= -v tests
LINT := flake8
LINTFLAGS := jump

all: build

build: build_ext

build_ext: _jump.so

_jump.so: jump/jump.cpp jump/jump.h jump/jumpmodule.c
	$(PYTHON) setup.py build_ext --inplace

test: build_ext
	$(TESTRUNNER) $(TESTRUNNERFLAGS)

test-all:
	tox --skip-missing-interpreters

.PHONY: lint
lint:
	$(LINT) $(LINTFLAGS)

.PHONY: clean
clean:
	$(RM) _jump*.so
	$(RM) -r build dist *.egg-info docs/_build .tox
	find . -name "*.py[co]" -delete
	find . -name __pycache__ | xargs rm -rf

.PHONY: docs
docs: build_ext
	$(MAKE) -C $@ html
