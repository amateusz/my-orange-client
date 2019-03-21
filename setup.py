from distutils.core import setup

from setuptools import find_packages

setup(
    name='my_orange_client',
    version='1.2.6',
    # packages=['my_orange_client'],
    packages=find_packages(),
    url='https://github.com/amateusz/my-orange-client',
    license='ffa',
    author='amateusz',
    author_email='grzywomat@gmail.com',
    description='A little tool to login to "My Orange" mobile operator account and check how much internet you have left for example',
    # long_description=open('README.md').read(),
    install_requires=[
        'requests_oauthlib',
        'requests',
        'bs4',
        # 'urllib.parse',  # python3 specific
        # 'getpass'
    ]
)
