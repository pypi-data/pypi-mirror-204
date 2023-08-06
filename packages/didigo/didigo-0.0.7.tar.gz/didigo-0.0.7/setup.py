#!/usr/bin/env python
# Copyright (c) didigo. All rights reserved.
from setuptools import find_packages, setup

from didigo.constant.version import version
import didigo.utils as utils


setup(
    name='didigo',
    version=version,
    description='didigo',
    long_description= utils.get_file_content("README.md"),
    long_description_content_type='text/markdown',
    author='didigo contributors',
    author_email='myname@example.com',
    keywords='didigo,  ll',
    url='https://github.com/xxx/xxxx',
    # packages=find_packages(exclude=('configs', 'tools', 'demo')),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    license='Apache License 2.0',
    # install_requires=utils.parse_requirements('requirements/runtime.txt'),
    # extras_require={
    #     'tests': utils.parse_requirements('requirements/tests.txt'),
    #     'build': utils.parse_requirements('requirements/build.txt'),
    #     'optional': utils.parse_requirements('requirements/optional.txt'),
    # },
    entry_points={
        'console_scripts': [
              'didigoy = didigo.cli:main'
          ]
    },
    ext_modules=[],
)
