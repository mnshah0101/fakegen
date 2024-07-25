from setuptools import find_packages, setup

setup(
    name='FakeGen',
    packages=find_packages(include=['fakegen']),
    version='0.1.0',
    description='A simple package to generate fake data with AI',
    author='Moksh Shah',
    install_requires=['anthropic==0.31.2'],
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=['pytest==8.3.1'],
    test_suite='tests',


)
