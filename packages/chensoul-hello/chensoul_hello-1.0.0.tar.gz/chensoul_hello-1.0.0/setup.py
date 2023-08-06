from setuptools import setup, find_packages

setup(
    name='chensoul_hello',
    version='1.0.0',
    author='John Doe',
    author_email='john.doe@example.com',
    description='A simple Python package',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.16.0',
        'pandas>=0.23.4',
    ],
    entry_points={
        'console_scripts': [
            'hello_command=chensoul_hello.cli:main',
        ],
    },
)
