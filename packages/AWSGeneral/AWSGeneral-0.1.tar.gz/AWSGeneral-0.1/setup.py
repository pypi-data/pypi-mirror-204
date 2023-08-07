from setuptools import setup, find_packages

setup(
    name='AWSGeneral',
    version='0.1',
    description='AWS pen testing tool',
    author='Bentalem',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
)

