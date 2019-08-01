from setuptools import setup, find_packages
from redash_py import __VERSION__


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_txt = f.read()


def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name='redash-py',
    version=__VERSION__,
    description='redash api client.',
    entry_points={
        "console_scripts": [
            "redashpy = redash_py.command:main"
        ]
    },
    long_description=readme,
    author='denzow',
    author_email='denzow@gmail.com',
    url='https://github.com/denzow/redash-py',
    license=license_txt,
    packages=find_packages(exclude=('sample',)),
    install_requires=_requires_from_file('requirements.txt'),
)
