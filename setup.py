from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in heero/__init__.py
from heero import __version__ as version

setup(
	name="heero",
	version=version,
	description="app for alltargeting",
	author="Heero",
	author_email="menaheero@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
