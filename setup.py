#!/usr/bin/env python3
#setup.py
import sys, os
from distutils.core import setup
from setuptools import setup
from setuptools.command.install import install

__version__ = "0.9"

#def readme():
#    with open(r"docs/README.md") as f:
#        return f.read()

setup(
    name = "MergeMail",
    description='A Mail Merge program for Gmail that allows attachments and dynamic placeholder text',
    version=__version__,
    url='https://github.com/Ghostom998/MergeMail.git',
    author='Thomas Roberts',
    author_email='tom_roberts.1992@hotmail.co.uk',
    license='GNU GPL V3.0',
    packages=['MergeMail'],
    install_requires=['pandas','tkinter','smtplib','csv','docx','python-docx','email','getpass'], # Dependencies
    python_requires='>=3.6.4',
    include_package_data=True,
    zip_safe=True,
#   long_description=readme(),
    entry_points = {
        'console_scripts': ['mergemail=mergemail.__init__:main'],
    },
    classifiers=[
    'Development Status :: 1 - Planning',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.6',
    'Environment :: Console',
    'Topic :: Office/Business :: Office Suites',
    ]
)