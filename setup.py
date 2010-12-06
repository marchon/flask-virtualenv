#!/usr/bin/env python
"""
https://github.com/imlucas/flask-virtualenv
"""

from setuptools import setup

setup(
    name='Flask-Virtualenv',
    version='0.1.1',
    url='http://imlucas.com',
    license='BSD',
    author='Lucas Hrabovsky',
    author_email='hrabovsky.lucas@gmail.com',
    description='Manage a virtualenv for your flask app.',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.6',
        'virtualenv>=1.5.1'
    ],
    test_suite='nose.collector',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: {{ license }} License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
