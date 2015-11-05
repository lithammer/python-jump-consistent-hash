PYTHON ?= python

all: build

build_ext: _jump.so

_jump.so: jump/jump.cpp jump/jump.h jump/jumpmodule.c
	$(PYTHON) setup.py build_ext --inplace

test: build_ext
	$(PYTHON) setup.py test

clean:
	rm -rfv build dist *.egg-info *.so
