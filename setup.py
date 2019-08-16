# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the contentui Sphinx extension.
'''

requires = ['Sphinx>=2.0']

setup(
    name='sphinxcontrib-contentui',
    version='0.2.4',
    url='https://github.com/ulrobix/sphinxcontrib-contentui',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-contentui',
    license='BSD',
    author='Robert Khaliullov',
    author_email='ulrobix@gmail.com',
    description='Sphinx "contentui" extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)