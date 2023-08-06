from pathlib import Path

from setuptools import find_packages
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="GooseMPL",
    license="MIT",
    author="Tom de Geus",
    author_email="tom@geus.me",
    description="Style and extension functions for matplotlib",
    long_description=long_description,
    keywords="matplotlib, style",
    url="https://github.com/tdegeus/GooseMPL",
    packages=find_packages(),
    use_scm_version={"write_to": "GooseMPL/_version.py"},
    setup_requires=["setuptools_scm"],
    install_requires=["deprecation", "matplotlib", "numpy", "pyyaml", "scipy"],
)
