import setuptools

with open('README.md', 'r') as fh:
  long_description = fh.read()

setuptools.setup(
  name = 'yzhanurlparser',
  version = '0.1.0',
  author = 'mantoufan',
  author_email = 'mhjlw@126.com',
  description = 'A python library which could parse URL to ip and country.',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/mantoufan/yzhanurlparser',
  packages = setuptools.find_packages(),
  classifiers = [
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
  ],
  python_requires = '>=3.6',
  install_requires = ['IP2Location'],
  include_package_data = True
)