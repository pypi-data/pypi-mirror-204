from setuptools import setup
import os

with open('README.md') as file:
    long_description = file.read()

setup(
    name='Timeseries-Preprocess',
    version='0.0.0',
    description='toolkit for time series preprocessing',
    author='Rui Wan',
    author_email='rwan972000@gamil.com',
    url='https://github.com/Kiko-RWan/Timeseries-Preprocess',
    packages=['timeseries_preprocess'],
    license='MIT',
    long_description_content_type="text/markdown",
    long_description=long_description
)