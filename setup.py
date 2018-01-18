#! /usr/bin/env python3

import os
from setuptools import setup


def get_long_description(file_name: str) -> str:
    """Gets the long description from the specified file's name.

    :param file_name: The file's name
    :type file_name: str
    :return: The content of the file
    :rtype: str
    """
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


if __name__ == '__main__':
    setup(
        name='ulaval-notify',
        version='0.1.0',
        description='Display monPortail notifications',
        author='Antoine Gagné',
        author_email='antoine.gagne.2@ulaval.ca',
        url='https://github.com/AntoineGagne/ulaval-notify',
        keywords='notifications',
        zip_safe=False,
        platforms='any',
        python_requires='>=3',
        packages=[
            'ulaval_notify',
            'ulaval_notify.api'
        ],
        entry_points={
            'console_scripts': ['ulaval-notify = ulaval_notify.main:main']
        },
        license='MIT',
        data_files=[],
        include_package_data=True,
        long_description=get_long_description('README.rst'),
        tests_require=[
            'pytest-runner',
            'pytest>=3.3.2',
            'tox',
            'coverage'
        ],
        test_suite='tests',
        scripts=[],
        classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Operating System :: Unix',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
        ],
        install_requires=[
            'requests>=2.18.4',
            'notify2>=0.3.1;sys_platform=="linux"',
            'dbus-python>=1.2.4;sys_platform=="linux"'
        ],
        extras_require={
            'daemon': ['python-daemon>=2.1.2'],
            'dev': [
                'flake8',
                'pylint',
                'Sphinx'
            ]
        }
    )
