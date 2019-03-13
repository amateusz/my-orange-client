from distutils.core import setup

setup(
    name='My Orange client',
    version='1.1',
    packages=[],
    url='https://github.com/amateusz/my-orange-client',
    license='ffa',
    author='amateusz',
    author_email='grzywomat@gmail.com',
    description='A little tool to login to "My Orange" mobile operator account and check how much internet you have left for example',
    # long_description=open('README.md').read(),
    requires=[
        'requests_oauthlib',
        'requests',
        'bs4',
        'urllib.parse',  # python3 specific
        'getpass'
    ]
)
