cmake_minimum_required(VERSION 3.15)

# Written into build-dir for the compile_commands.json target.
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION} LANGUAGES C)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

Python_add_library(_jump MODULE src/jump/jump.c WITH_SOABI)

# Must match the `from ._jump import ...` in src/jump/__init__.py.
install(TARGETS _jump DESTINATION jump)
