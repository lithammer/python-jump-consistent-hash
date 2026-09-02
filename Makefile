VIRTUALENV = .venv

.PHONY: all build clean lint test

all: build

compile_commands.json: CMakeLists.txt pyproject.toml src/jump/jump.c $(VIRTUALENV)/uv.lock
	uv pip install -e file://$(CURDIR)
	cp build/compile_commands.json $@

build: $(VIRTUALENV)/uv.lock
	uv pip install -e file://$(CURDIR)

$(VIRTUALENV)/uv.lock: uv.lock pyproject.toml
	uv sync
	@cp $< $@

test: build
	uv run -- pytest -v

lint: build
	uv run -- ruff check $(CURDIR)
	uv run -- ruff format --check --diff $(CURDIR)
	uv run -- ty check $(CURDIR)
	uv run -- clang-format --dry-run --Werror --style=file src/jump/*.c

clean:
	git clean -Xdf
