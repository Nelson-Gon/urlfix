from setuptools import setup, find_packages


setup(name='urlfix',
      version="0.1.1",
      description='Check and Fix Outdated URLs',
      url="http://www.github.com/Nelson-Gon/urlfix",
      download_url="https://github.com/Nelson-Gon/urlfix/archive/v0.1.0.zip",
      author='Nelson Gonzabato',
      author_email='gonzabato@hotmail.com',
      license='MIT',
      keywords="development url https markdown web",
      packages=find_packages(),
      long_description=open('README.md', encoding="utf-8").read(),
      long_description_content_type='text/markdown',
      install_requires=[],
      python_requires='>=3.6',
      zip_safe=False)
