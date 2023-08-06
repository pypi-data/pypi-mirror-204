from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'karmaMC is module that interacts with .adeth '

# Setting up
setup(
    name="karmaMC",
    version=VERSION,
    author="greysonapepin",
    author_email="greysonapepin@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['time', 'pyautogui', 'colorama', 'keyboard'],
    keywords=['python', 'video', 'minecraft'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)