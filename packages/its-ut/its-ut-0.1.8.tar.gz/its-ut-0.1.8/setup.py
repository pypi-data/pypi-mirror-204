from setuptools import setup, find_packages

VERSION = "0.1.8"

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
]


PYTHON_REQUIRES = ">=3.9"

INSTALL_REQUIRES = [
    "numpy",
    "networkx",
    "matplotlib",
]

setup(
    name="its-ut",
    version=VERSION,
    license="GPL-3.0",
    description="Framework with some work for the Information Theory & Statistics course at the University of Twente",
    author="Max Resing",
    author_email="pypi.org@maxresing.de",
    maintainer="Max Resing",
    maintainer_email="git@maxresing.de",
    url="https://gitlab.utwente.nl/s2300257/information-theory-q3",
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    python_requires=PYTHON_REQUIRES,
    entry_points={
        "console_scripts": [
            "its-ut=its.main:main"
        ]
    },
    classifiers=CLASSIFIERS,
)
