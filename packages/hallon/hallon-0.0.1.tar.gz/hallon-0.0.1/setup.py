from setuptools import setup


def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


setup(
    name="hallon",
    version="0.0.1",
    description="hallon is a package for network debugging",
    long_description=readfile('README.md'),
    long_description_content_type='text/markdown',
    author="Ryan Alloriadonis",
    author_email="yuantai78@gmail.com",
    url="https://github.com/RyanYuanSun/hallon",
    py_modules=['hallon'],
    python_requires='>=3.7',
    packages=['hallon'],
    license=readfile('LICENSE'),
    install_requires=[
      ],
    entry_points={
        'console_scripts': ['hallon=hallon:cmd', 'hallon-tools=hallon:cmd_tool']
        },
)