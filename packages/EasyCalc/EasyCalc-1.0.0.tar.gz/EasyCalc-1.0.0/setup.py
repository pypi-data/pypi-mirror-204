from setuptools import setup, find_packages

setup(
    name="EasyCalc",
    version="1.0.0",
    description="A simple Python library for creating a calculator with a GUI",
    author="RUBRUSH",
    author_email="askarsalikov58@gmail.com",
    url="https://github.com/RUBRUSH/EasyCalc",
    packages=find_packages(),
    install_requires=[
        "tkinter",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)