from setuptools import setup

# https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="rous",
    version="0.1.0",
    author="chris-c-mcintyre",
    author_email="chris-c-mcintyre@outlook.com",
    url="https://github.com/chris-c-mcintyre/rous",
    description="Doing things the hard way.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["rous"],
    package_dir={"rous": "src/rous"},
    install_requires=[""],
)
