import os

from setuptools import find_packages, setup

# ensure find_packages works if our current directory isn't this project
basedir = os.path.abspath(os.path.dirname(__file__))
os.chdir(basedir)
packages = find_packages(basedir)

requires = [
    'Flask==0.10.1',
    'python-dateutil',
    'pytz',
]

setup(
    name='baby-log',
    version='0.1',
    description='Track baby events like feedings',
    author='Andy Doan',
    license='AGPL',
    packages=packages,
    test_suite='tests',
    install_requires=requires,
    test_requires=['mock'],
)
