from setuptools import setup

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding='UTF-8') as fh:
    requirements = fh.read().split("\n")

from config import version

setup(
    name="D3adC0re Tools",
    version=version,
    description="D3adC0re Tools",
    author="Purpl3",
    author_email="d3adc0re@suntimedev.com",
    license="MIT",
    packages=["d3adc0re_tools"],
    include_package_data=True,
    install_requires=["googlesearch-python"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)