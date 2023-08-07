#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

tests_require = [
    'pytest',
    'pytest-mock'
]

dev_require = [
    *tests_require,
    'flake8',
    'flake8-comprehensions',
    'flake8-deprecated',
    'flake8-mutable',
    'flake8-tuple',
    'pytest-cov',
    'pyyaml',
    'twine',
    'wheel'
]

install_requires = ['pip', 'setuptools']

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
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities'
    ],
    description="this is my app",
    entry_points={
        'console_scripts': [
            'app02=app02.__main__:main',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='app02',
    name='app02',
    packages=find_packages(include=['app02', 'app02.*']),
    url='https://github.com/near2sea/app02',
    version='0.1.0',
    zip_safe=False,
)
