

from __future__ import print_function

from setuptools import setup


setup(
    name='cloudconvert',
    version='1.0.0',
    url='https://github.com/cloudconvert/cloudconvert-python',
    license='MIT',
    author='Josias Montag',
    tests_require=['nosetests'],
    author_email='info@cloudconvert.com',
    description='Official CloudConvert API wrapper',
    packages=['cloudconvert'],
    include_package_data=True,
    platforms='any',
    zip_safe=False,
    keywords=["cloudconvert", "convert"],
    install_requires = ['requests>=2.3.0'],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Archiving :: Packaging",
        ],
)