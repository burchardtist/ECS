from distutils.core import setup

readme = open('README.md').read()

setup(
    name='byt',
    version='0.3.0',
    author='Aleksander Philips',
    author_email='aleksander.philips at gmail.com',
    packages=['byt'],
    url='https://github.com/burchardtist/byt',
    license='MIT',
    description='The ECS architecture',
    long_description=readme,
    install_requires=[
        'panek-db==1.0.0',
    ],
    dependency_links=[
        'git+ssh://git@github.com/burchardtist/panek_db.git#egg=panek-db==1.0.0',
    ]
)
