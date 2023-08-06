from setuptools import setup, find_packages
import os
import platform
from urllib import request, parse

setup(
    name='ceedeetest',
    version='0.0.1',
    license='MIT',
    author="",
    author_email='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='ceedee project',
    install_requires=[
          'scikit-learn',
          'requests',
      ],
)
