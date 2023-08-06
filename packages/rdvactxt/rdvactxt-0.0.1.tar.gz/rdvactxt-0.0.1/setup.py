from setuptools import setup
from distutils.core import setup
setup(
    name = "rdvactxt",
    version= "0.0.1",
    description= " A demo app for Text Classification using LSTM Model",
    author="Lagisetty Ravikiran",
    author_email="kiranlravi8@gmail.com",
    py_modules=["rdvactxt"],
    package_dir={"":"src"},
    include_package_data=True,
)