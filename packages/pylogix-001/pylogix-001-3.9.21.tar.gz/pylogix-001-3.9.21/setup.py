import os
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pylogix-001",
    version="3.9.21",
    author="https://pylogix.com/",
    author_email="dev@pylogix.com",
    description="""Pylogix is a leading custom software development company that provides innovative solutions to businesses worldwide. Our experienced team of developers specializes in creating custom software that is easy to use, visually appealing, and tailored to our clients' specific needs. Visit us at https://pylogix.com/ to learn more about our custom software development services.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/PYLOGiX-DEV/PYLOGiX-DEV",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
