VIRTUALENV = .venv

.PHONY: all build clean lint test

all: build

# Configured into its own directory: scikit-build-core builds `build/`
# with Ninja, and reconfiguring that with another generator breaks it.
compile_commands.json: CMakeLists.txt pyproject.toml src/jump/jump.c | build
	cmake -B .cmake-build -S $(CURDIR) -DCMAKE_BUILD_TYPE=Release \
		-DPython_EXECUTABLE=$(VIRTUALENV)/bin/python
	cp .cmake-build/compile_commands.json $@

build:
	uv sync

test: build
	uv run -- pytest -v

lint: build
	uv run -- ruff check $(CURDIR)
	uv run -- ruff format --check --diff $(CURDIR)
	uv run -- ty check $(CURDIR)
	uv run -- clang-format --dry-run --Werror --style=file src/jump/*.c

clean:
	git clean -Xdf
