from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="selenium-kit",
    version="0.0.3",
    license="MIT",
    author="Yash Jain",
    author_email="yash0307jain@gmail.com",
    description="Selenium kit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/yash0307jain/selenium-kit",
)
