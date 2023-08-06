from setuptools import setup, find_packages

setup(
    name='graph-model-parser',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
    ],
    author='Albert Buchard',
    description='A package for parsing and evaluating dynamical graph models',
    url='https://github.com/albertbuchard/GraphModelParser',
)
