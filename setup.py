# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="app-store-server-library",
    version="1.5.0",
    description="The App Store Server Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.7, <4",
    install_requires=["attrs >= 21.3.0", 'PyJWT >= 2.6.0, < 3', 'requests >= 2.28.0, < 3', 'cryptography >= 40.0.0', 'pyOpenSSL >= 23.1.1', 'asn1==2.7.0', 'cattrs >= 23.1.2'],
    extras_require={
        "async": ["httpx"],
    },
    package_data={"appstoreserverlibrary": ["py.typed"]},
    license="MIT",
    classifiers=["License :: OSI Approved :: MIT License"],
)
