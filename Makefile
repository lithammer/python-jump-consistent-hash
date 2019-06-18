PYTHON ?= python
TESTRUNNER ?= tox
TESTRUNNERFLAGS ?= -v tests
LINT := flake8
LINTFLAGS := jump

PLATFORMS = manylinux1_x86_64 manylinux1_i686 manylinux2010_x86_64

all: build

build: _jump.so

_jump.so: jump/jump.c
	$(PYTHON) setup.py build_ext --inplace

.PHONY: test
test:
	$(TESTRUNNER) $(TESTRUNNERFLAGS)

.PHONY: wheels
wheels: $(PLATFORMS)
ifeq ($(shell uname -s),Darwin)
	# https://github.com/drolando/homebrew-deadsnakes
	python2.7 -m pip wheel $(CURDIR) -w wheelhouse
	python3.4 -m pip wheel $(CURDIR) -w wheelhouse
	python3.5 -m pip wheel $(CURDIR) -w wheelhouse
	python3.6 -m pip wheel $(CURDIR) -w wheelhouse
	python3.7 -m pip wheel $(CURDIR) -w wheelhouse
endif

$(PLATFORMS):
	docker pull quay.io/pypa/$@
	[ $@ = manylinux1_i686 ] && PRE_CMD=linux32; \
		docker run --rm -e PLAT=$@ -v $(CURDIR):/shared \
			quay.io/pypa/$@ $$PRE_CMD /shared/build-wheels.sh

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
