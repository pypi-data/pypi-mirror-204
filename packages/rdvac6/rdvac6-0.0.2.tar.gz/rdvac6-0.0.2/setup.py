from setuptools import setup
from distutils.core import setup
setup(
    name = "rdvac6",
    version= "0.0.2",
    description= " A demo app for Text Classification using LSTM Model",
    author="Lagisetty Ravikiran",
    author_email="kiranlravi8@gmail.com",
    py_modules=["rdvac6"],
    package_dir={"":"src"},
    include_package_data=True,
)