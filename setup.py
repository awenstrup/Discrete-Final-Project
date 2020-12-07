from setuptools import setup, find_packages

setup(
    name='hamming',
    version='0.0.1',
    packages=find_packages(include=["hamming"]),
    install_requires=[
        "numpy",
        "bitarray"
    ]
)