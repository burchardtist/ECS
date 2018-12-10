from distutils.core import setup

readme = open('README.md').read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='byt',
    version='0.1.1',
    author='Aleksander Philips',
    author_email='aleksander.philips at gmail.com',
    packages=['byt'],
    url='https://github.com/burchardtist/byt',
    license='MIT',
    description='The ECS architecture',
    long_description=readme,
    install_requires=required,
)
