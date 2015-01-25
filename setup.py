# coding=utf-8
import setuptools

def package_data_dirs(source, sub_folders):
	import os
	dirs = []

	for d in sub_folders:
		for dirname, _, files in os.walk(os.path.join(source, d)):
			dirname = os.path.relpath(dirname, source)
			for f in files:
				dirs.append(os.path.join(dirname, f))

	return dirs

def params():
	name = "OctoPrint-Android-Connect"
	version = "0.1.1"

	description = "Adds support for connectivity setup within OctoPrint"
	long_description = "TODO"
	author = "Extensio"
	author_email = "info@extensio.ru"
	url = "http://extensio.ru"
	license = "AGPLv3"

	packages = ["android_connect"]
	package_data = {"android_connect": package_data_dirs('android_connect', ['static', 'templates'])}

	include_package_data = True
	zip_safe = False
	install_requires = open("requirements.txt").read().split("\n")

	entry_points = {
		"octoprint.plugin": [
			"android_connect = android_connect"
		]
	}

	return locals()

setuptools.setup(**params())
