from setuptools import find_packages, setup
from llmbda_fastapi import __version__

def read_requirements():
    with open('requirements.txt') as req_file:
        requirements = req_file.read().splitlines()
    return requirements

setup(
    name="llmbda_fastapi",
    version=__version__,
    url="https://relevanceai.com/",
    author="Relevance AI",
    author_email="jacky@relevanceai.com",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    setup_requires=["wheel"],
    install_requires=read_requirements(),
    package_data={"": ["*.ini"]},
    extras_require=dict(),
)
