from setuptools import setup

setup(
    name='mongo_db_operation',
    version='1.0.3',
    description='My MongoDB package',
    author='Melih Teke',
    packages=['src/mongo_db_operation'],
    install_requires=[
        'pymongo'
    ],
)
