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
	version = "0.1.0"

	description = "Adds support for connectivity setup within OctoPrint"
	long_description = "TODO"
	author = "Extensio"
	author_email = "info@extensio.ru"
	url = "http://extensio.ru"
	license = "AGPLv3"

	packages = ["octoprint_android_connect"]
	package_data = {"octoprint_android_connect": package_data_dirs('octoprint_android_connect', ['static', 'templates'])}

	include_package_data = True
	zip_safe = False
	install_requires = open("requirements.txt").read().split("\n")

	entry_points = {
		"octoprint.plugin": [
			"android_connect = octoprint_android_connect"
		]
	}

	return locals()

setuptools.setup(**params())
