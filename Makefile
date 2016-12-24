PYTHON ?= python
LINT := flake8
LINTFLAGS := jump

all: build_ext

build_ext: _jump.so

_jump.so: jump/jump.cpp jump/jump.h jump/jumpmodule.c
	$(PYTHON) setup.py build_ext --inplace

test: build_ext
	$(PYTHON) setup.py test

test-all:
	tox --skip-missing-interpreters

.PHONY: lint
lint:
	$(LINT) $(LINTFLAGS)

.PHONY: clean
clean:
	$(RM) _jump.so
	$(RM) -r build dist *.egg-info docs/_build .tox

.PHONY: docs
docs: build_ext
	$(MAKE) -C $@ html
