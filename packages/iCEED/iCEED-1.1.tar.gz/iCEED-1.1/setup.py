import setuptools
from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='iCEED',
    version='1.1',
    author='Rajiv Karbhal',
    author_email='rajivkarbhal@gmail.com',
    description='Package for customized extraction of enzyme data from bioinformatics databases',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=[
        'requests',
    ],
    package_data={
        'iCEED': ['Examples/*.py'],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)