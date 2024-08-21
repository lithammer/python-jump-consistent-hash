VIRTUALENV = .venv

all: build

compile_commands.json: build
	bear -- uv run -- python setup.py build_ext -qf

build: $(VIRTUALENV)/uv.lock

$(VIRTUALENV)/uv.lock: uv.lock pyproject.toml
	uv sync
	@cp $< $@

.PHONY: test
test: build
	uv run -- pytest -v

.PHONY: lint
lint: build
	uv run -- ruff check --diff $(CURDIR)
	uv run -- ruff format --check --diff $(CURDIR)
	uv run -- mypy $(CURDIR)
	clang-format --dry-run --Werror --style=file src/jump/*.c

.PHONY: clean
clean:
	git clean -Xdf
