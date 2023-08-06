#!/usr/bin/env python

from setuptools import setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ovinc_client",
    version="0.0.1",
    author="OVINC",
    url="https://www.ovinc.cn/",
    author_email="contact@ovinc.cn",
    description="A Tool for OVINC Union API",
    packages=["ovinc_client", "ovinc_client.components"],
    install_requires=[
        "requests==2.27.1",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
