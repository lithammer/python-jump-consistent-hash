VIRTUALENV = .venv
UV_RUN = uv run --

all: build

compile_commands.json: build
	bear -- $(UV_RUN) python setup.py build_ext -qf

build: $(VIRTUALENV)/uv.lock

$(VIRTUALENV)/uv.lock: uv.lock pyproject.toml
	uv sync
	@cp $< $@

.PHONY: test
test: build
	$(UV_RUN) pytest -v

.PHONY: lint
lint: build
	$(UV_RUN) ruff check --diff $(CURDIR)
	$(UV_RUN) ruff format --check --diff $(CURDIR)
	$(UV_RUN) mypy $(CURDIR)
	clang-format --dry-run --Werror --style=file src/jump/*.c

.PHONY: clean
clean:
	git clean -Xdf
