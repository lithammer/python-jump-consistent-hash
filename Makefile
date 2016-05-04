PYTHON ?= python

all: build_ext

build_ext: _jump.so

_jump.so: jump/jump.cpp jump/jump.h jump/jumpmodule.c
	$(PYTHON) setup.py build_ext --inplace

test: build_ext
	$(PYTHON) setup.py test

test-all:
	tox --skip-missing-interpreters

clean:
	rm -rfv build dist *.egg-info *.so docs/_build

.PHONY: docs
docs: build_ext
	$(MAKE) -C docs html
