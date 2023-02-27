from __future__ import annotations

from setuptools import setup


def find_required():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    version='0.0.2',
    install_requires=find_required(),
)
