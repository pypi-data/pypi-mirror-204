import setuptools
from pathlib import Path

setuptools.setup(
    name="scottpdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    # automatically finds the pacakages
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
