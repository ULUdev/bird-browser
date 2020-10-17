from setuptools import setup
setup(
    name="birdlib",
    version="1.0.0",
    description="the library for bird-browser",
    url="https://github.com/ULUdev/bird-browser",
    author="ULUdev",
    license="GNU GPL 3.0",
    packages=["birdlib"],
    include_package_data=True,
    install_requires=["PyQt5", "PyQtWebEngine", "requests"]
)
