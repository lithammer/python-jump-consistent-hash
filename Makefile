BINDIR = $(VIRTUALENV)/bin
PYTHON ?= python3
VIRTUALENV = .venv

all: build

compile_commands.json:
	bear -- $(PYTHON) setup.py build_ext -qf

.PHONY: build
build: $(VIRTUALENV)/freeze.txt

$(VIRTUALENV): $(VIRTUALENV)/freeze.txt
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
	$(BINDIR)/tox -e black,mypy,ruff

.PHONY: clean
clean:
	git clean -Xdf
