#!/usr/bin/env python

from distutils.core import setup

setup(
    name='my-orange-client',
    version='0.4',
    packages=[''],
    url='https://github.com/amateusz/my-orange-client',
    license='ffa',
    author='amateusz',
    author_email='grzywomat@gmail.com',
    description='A little tool to login to "My Orange" mobile operator account and check how much internet you have left for example',
    install_requires=[
        'requests_oauthlib',
        'requests',
        'bs4',
        'json',
        'urllib.parse',  # python3 specific
        'getpass'
    ]
)
