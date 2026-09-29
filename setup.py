from setuptools import find_packages, setup

setup(
	name="seven_habits",
	version="0.0.1",
	description="Personal alignment, planning, evidence and review for Frappe",
	author="Felix",
	packages=find_packages(),
	include_package_data=True,
	install_requires=["frappe"],
)
