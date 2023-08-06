from setuptools import setup, find_packages
import os
os.chdir(r'C:\Users\JustBNF\Desktop\Secret~\Python\Modules\ChatAIMaker')
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]

setup(
    name = "chataimaker",
    version = "1.3",
    description = "Package, that can help make you AI chat bot",
    long_description = open("README.txt").read() + '\n\n\n' + open("CHANGELOG.txt").read(),
    url="",
    author="Boynfriend",
    author_email="justbnf@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords='',
    packages=find_packages(),
    install_requires=['nltk', 'numpy', 'tflearn', 'tensorflow']
)
