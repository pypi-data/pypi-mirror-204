#!/usr/bin/env python3

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

tests_require = [
    'pytest',
    'responses',
    'pytest-mock',
    'werkzeug<2.1.0'
]
dev_require = [
    *tests_require,
    'flake8',
    'flake8-comprehensions',
    'flake8-deprecated',
    'flake8-mutable',
    'flake8-tuple',
    'twine',
    'wheel',
    'oss2'
]

install_requires = [
    'pip',
    'setuptools'
]

# bdist_wheel
extras_require = {
    'dev': dev_require,
    'test': tests_require
}

setup(
    author="lihaijian",
    author_email='sanan.li@qq.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="my first app01",
    entry_points={
        'console_scripts': [
            'app01=app01.cli:main',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='app01',
    name='app01',
    packages=find_packages(include=['app01', 'app01.*']),
    url='https://github.com/near2sea/app01',
    version='0.1.6',
    zip_safe=False,
)
