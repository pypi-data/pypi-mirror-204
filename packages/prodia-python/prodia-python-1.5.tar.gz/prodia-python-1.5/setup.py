from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='prodia-python',
version='1.5',
description='Prodia API Python Wrapper',
long_description=long_description,
long_description_content_type='text/markdown',
author='yoou3-cyber',
author_email='zenafey@eugw.ru',
packages=['prodia'],
license='MIT',
install_requires=['requests'])
