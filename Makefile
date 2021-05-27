BINDIR = $(VIRTUALENV)/bin
PYTHON ?= python3
VIRTUALENV = venv

all: test

compile_commands.json:
	bear -- $(PYTHON) setup.py build_ext -qf

.PHONY: venv
venv: $(VIRTUALENV)/freeze.txt

$(VIRTUALENV)/freeze.txt: requirements.txt
	$(PYTHON) -m venv $(@D)
	$(BINDIR)/pip install -U pip setuptools wheel
	$(BINDIR)/pip install -r $< -e $(CURDIR)
	$(BINDIR)/pip freeze -r $< > $@

.PHONY: test
test: $(VIRTUALENV)
	$(BINDIR)/tox

.PHONY: lint
lint: $(VIRTUALENV)
	$(BINDIR)/black --check src
	$(BINDIR)/flake8 src
	$(BINDIR)/mypy src

.PHONY: clean
clean:
	git clean -Xdf
