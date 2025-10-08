VIRTUALENV = .venv

.PHONY: all build clean lint test

all: build

compile_commands.json: build
	bear -- uv run -- python setup.py build_ext -qf

build: $(VIRTUALENV)/uv.lock
	uv pip install -e file://$(CURDIR)

$(VIRTUALENV)/uv.lock: uv.lock pyproject.toml
	uv sync
	@cp $< $@

test: build
	uv run -- pytest -v

lint: build
	uv run -- ruff check --diff $(CURDIR)
	uv run -- ruff format --check --diff $(CURDIR)
	uv run -- mypy $(CURDIR)
	clang-format --dry-run --Werror --style=file src/jump/*.c

clean:
	git clean -Xdf
