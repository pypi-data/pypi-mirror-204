# Description: Setup script for the qbf_index package
from setuptools import setup, find_packages

setup(
    name='btree_index',
    version='0.1.0',
    author='Mohamed Diomande',
    author_email='gdiomande7907@gmail.com',
    description='Python package for implementing a B-Tree',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/diomandeee/btree_index',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
            'numpy',
            'scipy'
        ],
)
