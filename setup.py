from __future__ import annotations

from setuptools import setup


def find_required():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    version='0.0.1',
    install_requires=find_required(),
)
