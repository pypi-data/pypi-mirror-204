#!/usr/bin/env python

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    long_description = readme_file.read()

setup(
    name="netbox-network-diagram",
    version="0.1.2",
    description="A plugin to render network diagram in NetBox.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/entooone/netbox-network-diagram",
    author="entooone",
    author_email="entooone@gmail.com",
    license="Apache License 2.0",
    install_requires=[],
    keywords=["netbox-plugin"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    project_urls={
        "Source": "https://github.com/entooone/netbox-network-diagram",
        "Tracker": "https://github.com/entooone/netbox-network-diagram/issues",
    },
    include_package_data=True,
    zip_safe=False,
)
