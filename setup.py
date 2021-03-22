from setuptools import setup, find_packages

from urlfix.version import __version__
setup(name='urlfix',
      version=__version__,
      description='Check and Fix Outdated URLs',
      url="http://www.github.com/Nelson-Gon/urlfix",
      download_url="https://github.com/Nelson-Gon/urlfix/",
      author='Nelson Gonzabato',
      author_email='gonzabato@hotmail.com',
      license='MIT',
      keywords="development url https markdown web url-validation url-checker",
      packages=find_packages(),
      long_description=open('README.md', encoding="utf-8").read(),
      long_description_content_type='text/markdown',
      install_requires=[],
      python_requires='>=3.6',
      zip_safe=False)
