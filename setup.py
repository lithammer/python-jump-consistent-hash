import os

from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension(
            "_jump",
            sources=["src/jump/jump.c"],
            optional=os.environ.get("CIBUILDWHEEL", "0") != "1",
        )
    ]
)
