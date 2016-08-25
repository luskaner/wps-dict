# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    custom_license = f.read()

setup(
    name='wps-dict',
    version='0.9.0',
    description='Utility to generate WPS pins based on different providers and tools',
    long_description=readme,
    author='David Fernández Aldana',
    author_email='luskaner@gmail.com',
    url='https://github.com/wps-dict/wps-dict',
    license=custom_license,
    packages=find_packages(exclude=('tests', 'docs'))
)
