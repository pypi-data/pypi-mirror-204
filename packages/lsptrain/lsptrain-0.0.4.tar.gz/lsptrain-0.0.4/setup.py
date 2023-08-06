from distutils.core import setup
from setuptools import find_packages

with open('README.rst', 'r', encoding="utf-8") as f:
    long_description = f.read()

setup(name='lsptrain',
      version='0.0.4',
      description='nlp for anyone',
      long_description=long_description,
      author='ykallan',
      author_email='815583442@qq.com',
      url='http://www.gitee.com/ykallan',
      install_requires=['torch>=1.10',
                        'transformers>=4.20.1',
                        'scikit-learn>=1.1.0',
                        'tqdm'],
      python_requires='>=3.7',
      license='BSD License',
      packages=find_packages(),
      platforms=['all'],
      include_package_data=True
      )
