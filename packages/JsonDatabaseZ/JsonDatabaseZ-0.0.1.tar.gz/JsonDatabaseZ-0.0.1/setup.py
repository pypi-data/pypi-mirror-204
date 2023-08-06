import pathlib
from setuptools import find_packages, setup


HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PAKAGE_NAME = 'JsonDatabaseZ'
AUTHOR = 'Rey Michel Del Toro Martinez'
AUTHOR_EMAIL = 'martinez200921@gmail.com'
URL = 'https://github.com/ReyDev2009'

LICENSE = 'MIT'
LONG_DESCRIPTION = (HERE/"README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"

setup(
    name=PAKAGE_NAME,
    version=VERSION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    include_package_data=True,
    long_description_content_type=LONG_DESC_TYPE,
    license=LICENSE,
    packages=find_packages()
)
