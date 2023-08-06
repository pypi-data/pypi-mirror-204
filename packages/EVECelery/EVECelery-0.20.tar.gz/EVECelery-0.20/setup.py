#!/usr/bin/env python

import setuptools

pkg_info = {}
with open("EVECelery/__version__.py", "r", encoding="utf-8") as f:
    for l in f.readlines():
        data = l.split('=')
        pkg_info[data[0].strip()] = (data[1].replace("'", "")).strip()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(name='EVECelery',
                 version=pkg_info['__version__'],
                 description=pkg_info['__description__'],
                 license=pkg_info['__license__'],
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 author_email=pkg_info['__author_email__'],
                 url='https://github.com/NullsecSpace/EVECelery',
                 project_urls={
                     'Documentation': 'https://EVECelery.nullsec.space',
                     'Source': 'https://github.com/NullsecSpace/EVECelery',
                     'Tracker': 'https://github.com/NullsecSpace/EVECelery/issues',
                 },
                 packages=setuptools.find_packages(include=["EVECelery", "EVECelery.*"]),
                 install_requires=[
                     'Celery~=5.2',
                     'pika~=1.3',
                     'python-dateutil~=2.8.2',
                     'redis~=4.1',
                     'requests~=2.27',
                     'pydantic~=1.10'
                 ],
                 python_requires=">=3.7",
                 entry_points={
                     'console_scripts': [
                         'eve-celery = EVECelery.__main__:main'
                     ]
                 },
                 classifiers=[
                     'Development Status :: 2 - Pre-Alpha',
                     'Programming Language :: Python :: 3.10',
                     'Topic :: Games/Entertainment',
                     'License :: OSI Approved :: MIT License',

                 ],
                 keywords='eve online rabbitmq esi redis message queue broker'
                 )
