from pathlib import Path
from setuptools import setup

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="bird-browser",
    version="1.0.3",
    description="a simple browser written in python with a lot of implementations",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ULUdev/bird-browser",
    author="ULUdev",
    license="GNU GPL 3.0",
    packages=["bird-browser"],
    include_package_data=True,
    install_requires=["PyQt5>=5.15.0", "PyQtWebEngine>=5.15.0", "birdlib>=0.5.2"]
)
