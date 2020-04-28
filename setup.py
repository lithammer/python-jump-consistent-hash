import io
import os

from setuptools import Extension, find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jump-consistent-hash",
    version="3.1.1",
    description="Implementation of the Jump Consistent Hash algorithm",
    long_description=long_description,
    author="Peter Lithammer",
    author_email="peter.lithammer@gmail.com",
    license="MIT",
    url="https://github.com/lithammer/python-jump-consistent-hash",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"jump": ["py.typed", "__init__.pyi"]},
    zip_safe=False,
    ext_modules=[
        Extension("_jump", sources=["src/jump/jump.c"], optional=True)
    ],
    keywords=[
        "jump hash",
        "jumphash",
        "jump consistent hash",
        "consistent hash",
        "hash algorithm",
        "hash",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
