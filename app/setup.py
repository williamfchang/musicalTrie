# https://flask.palletsprojects.com/en/2.0.x/patterns/distribute/

from setuptools import setup, find_packages

setup(
    name='musicalTrie',
    version='0.1',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)