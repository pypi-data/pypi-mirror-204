import pathlib
import sys
from setuptools import setup, find_packages


HERE = pathlib.Path(__file__).parent
VERSION = '0.0.5'
PACKAGE_NAME = 'oslili-cli'
AUTHOR = 'Oscar Valenzuela B.'
AUTHOR_EMAIL = 'oscar.valenzuela.b@gmail.com'
URL = 'https://github.com/oscarvalenzuelab/oslili-cli'
LICENSE = 'Apache-2.0'
DESCRIPTION = 'Open Source License Identification Library'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

setup(
    name=PACKAGE_NAME, 
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=['src'],
    entry_points={"console_scripts": ["oslili-cli=src.cli:main"]},
    install_requires=["oslili", ],
    url=URL,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License'
    ],
)
