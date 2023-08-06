from setuptools import setup, find_packages

setup(
    name="circleci-stubs",
    version="0.1",
    description="Type stubs for circleci",
    packages=find_packages(),
    install_requires=["circleci >= 1.2.2"],
    package_data={"circleci-stubs": ["py.typed"]},
)
