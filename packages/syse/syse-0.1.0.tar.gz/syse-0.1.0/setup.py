from setuptools import setup, find_packages
import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "syse",
    version = "0.1.0",
    author = "Jonathon Nicholson",
    author_email = "Jonathon@apexpromgt.com",
    description = "Systems & Industrial Engineering Python Package",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/apexpromgt/SysE",
    project_urls = {
        "Homepage": "https://github.com/apexpromgt/SysE",
        "Documentation": "https://syse.readthedocs.io/en/latest/",
        "Bug Tracker":"https://github.com/apexpromgt/SysE/issues"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.7",
    dependencies = ["numpy<=1.23.2"]
)