from setuptools import setup

setup(
    name='mpserializer',
    packages=['serializers', 'serializers/parsers'],
    version='2.0.0',
    description='my serializer',
    author='Carcajo',
    author_email='t375445391507@gmail.com',
    install_requires=['toml==0.10.2', 'PyYAML==5.4.1'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests/',
)
