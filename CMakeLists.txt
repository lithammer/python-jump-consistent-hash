cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION} LANGUAGES C)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

Python_add_library(_jump MODULE src/jump/jump.c WITH_SOABI)
install(TARGETS _jump DESTINATION ${SKBUILD_PROJECT_NAME})
