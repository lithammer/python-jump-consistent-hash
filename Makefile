VIRTUALENV = .venv

all: build

compile_commands.json: build
	bear -- rye run python setup.py build_ext -qf

build: $(VIRTUALENV)/requirements.lock

$(VIRTUALENV)/requirements.lock: requirements.lock requirements-dev.lock pyproject.toml
	rye sync
	@cp $< $@

.PHONY: test
test: build
	rye test -v

.PHONY: lint
lint: build
	rye run lint
	clang-format --dry-run --Werror --style=file src/jump/*.c

.PHONY: clean
clean:
	git clean -Xdf
