from setuptools import setup, find_packages
from codecs import open
from os import path

version = '0.8.1'
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
  long_description = f.read()
with open(path.join(here, 'LICENSE.txt'), encoding='utf-8') as f:
  license = f.read()

setup(
  name = 'ytools',
  packages = find_packages(),
  install_requires = ['PyYaml', 'jsonpath-ng', 'jsonschema'],
  version = '%s' % version,
  description = 'Command-line tool for selectively dumping nodes from `yaml` (or `json`) documents in `yaml` or `json` format.',
  long_description=long_description,
  author = 'Jakob Stemberger',
  author_email = 'yaccob@gmx.net',
  license = license,
  url = 'https://github.com/yaccob/ytools', # use the URL to the github repo
  download_url = 'https://github.com/yaccob/ytools/archive/%s.tar.gz' % version, # I'll explain this in a second
  keywords = ['yaml', 'json', 'python', 'jsonpath', 'json-path', 'dump', 'convert', 'validate', 'schema'],
  classifiers = ['Programming Language :: Python :: 2.7'],
  scripts = ['scripts/ytools'],
)
