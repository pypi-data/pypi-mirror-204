from setuptools import setup, find_packages

setup(
    name='python-common-package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'boto3'
    ],
)