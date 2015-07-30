all:

build:
	python setup.py build

_jump.so: jump/jump.cpp jump/jump.h jump/jumpmodule.c
	python setup.py build_ext --inplace

test: _jump.so
	python setup.py test

clean:
	rm -rfv build dist *.egg-info *.so
