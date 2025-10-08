VIRTUALENV = .venv

.PHONY: all build clean lint test

all: build

compile_commands.json: build
	cp $</compile_commands.json $@

build: $(VIRTUALENV)/uv.lock
	uv build --wheel

$(VIRTUALENV)/uv.lock: uv.lock pyproject.toml
	uv sync
	cp $< $@

test: build
	uv run -- pytest -v

lint: build
	uv run -- ruff check --diff $(CURDIR)
	uv run -- ruff format --check --diff $(CURDIR)
	uv run -- mypy $(CURDIR)
	clang-format --dry-run --Werror --style=file src/jump/*.c

clean:
	git clean -Xdf
