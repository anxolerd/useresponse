import re
import os.path

from setuptools import setup, find_packages


with open(
    os.path.join(os.path.dirname(__file__), 'useresponse', '__init__.py')
) as f:
    VERSION = re.match(r".*__version__ = '(.*?)'", f.read(), re.S).group(1)


setup(
    name='useresponse',
    version=VERSION,
    description='Python client for Useresponse',
    author='Oleksandr Kovalchuk',
    author_email='anxolerd@outlook.com',
    url='https://github.com/anxolerd/useresponse',
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
