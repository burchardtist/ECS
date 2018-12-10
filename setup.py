from distutils.core import setup

readme = open('README.md').read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='ecs',
    version='0.1.0',
    author='Aleksander Philips',
    author_email='aleksander.philips at gmail.com',
    packages=['ecs', 'supervisor'],
    url='https://github.com/burchardtist/game_engine',
    license='MIT',
    description='The ECS architecture',
    long_description=readme,
    install_requires=required,
)
