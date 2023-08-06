import os

from setuptools import find_packages, setup


def find_stubs(package):
    stubs = []
    for root, dirs, files in os.walk(package):
        for file in files:
            yield os.path.join(root, file).replace(package + os.sep, "", 1)


setup(
    name="circleci-stubs",
    version="0.1.2",
    description="Type stubs for circleci",
    packages=find_packages(),
    install_requires=["circleci >= 1.2.2"],
    package_data={"circleci-stubs": ["py.typed"] + list(find_stubs("circleci-stubs"))},
)
