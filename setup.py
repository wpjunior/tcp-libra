# -*- coding:utf-8 -*-

from setuptools import find_packages, setup

version = '0.1.0'

setup(
    name='tcp-libra',
    version=version,
    description='The simple tcp load balancer written in tornado',
    long_description='',
    classifiers=[],
    keywords='tcp load balancer',
    author='Wilson Junior',
    author_email='wilsonpjunior@gmail.com',
    url='https://github.com/wpjunior/tcplibra.git',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'tornado'
    ],
    entry_points={
        'console_scripts': ['tcp-libra=tcplibra.server:run'],
    }
)
