from setuptools import setup, find_packages

setup(
    name='common_as',
    version='1.3.1',
    description='common modules used in Arthasangraha suite of projects',
    author='Arthasangraha',
    author_email='roopesh@arthasangraha.com',
    packages=find_packages(),
    install_requires=[
        'ta-lib', 'pandas', 'numpy'
    ],
)
