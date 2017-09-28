import setuptools

setuptools.setup(
    name='locked',
    version='0.0.1',
    description='Locked - password manager',
    author='Piotr Wasilewski',
    author_email='piotrek@piotrek.io',
    packages=['locked'],
    scripts=['bin/locked'],
    install_requires=[
        'click==6.7',
        'pycrypto==2.6.1',
    ]
)
