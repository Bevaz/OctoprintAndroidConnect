# coding=utf-8
from __future__ import absolute_import

__author__ = "Extensio <info@extensio.ru>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2014 Extensio 3D Console - Released under terms of the AGPLv3 License"

import flask
import logging

import octoprint.plugin
import octoprint.events


class AndroidConnectPlugin(octoprint.plugin.EventHandlerPlugin,
                  octoprint.plugin.StartupPlugin,
                  octoprint.plugin.SimpleApiPlugin,
                  octoprint.plugin.SettingsPlugin,
                  octoprint.plugin.TemplatePlugin,
                  octoprint.plugin.AssetPlugin):
	def __init__(self):
		self.logger = logging.getLogger("octoprint.plugins." + __name__)

	#~~ StartupPlugin API

	def on_startup(self, host, port):
		self.logger.warn("Invoking <on_startup>")

	def on_after_startup(self):
		self.logger.warn("Invoking <on_after_startup>")


	#~~ TemplatePlugin API

	def get_template_vars(self):
		return dict(
			_settings_menu_entry="AndroidConnect"
		)

	def get_template_folder(self):
		import os
		return os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")

	##~~ AssetPlugin API

	def get_asset_folder(self):
		import os
		return os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")

	def get_assets(self):
		return {
			"js": ["js/android_connect.js"],
			"css": ["css/android_connect.css"],
			"less": ["less/android_connect.less"]
		}

	#~~ SimpleApiPlugin API

	def get_api_commands(self):
		return dict(
			execute=["shell"]
		)

	def on_api_command(self, command, data):
		if command == "execute":
			self.logger.error("Command test is invoked")
			import sarge
			command_str = data["shell"]
			self.logger.error("Executing command: %s" % command_str)
			try:
				p = sarge.run(command_str, stdout=sarge.Capture(), stderr=sarge.Capture())
				returncode = p.returncode
				stderr_text = p.stderr.text
				stdout_text = p.stdout.text
				if returncode == 0:
					self.logger.warn("Executed command success %r: <%s>-<%s>" % (returncode, stdout_text, stderr_text))
					return flask.jsonify(dict(success=True, msg=str(stdout_text)))
				else:
					self.logger.warn("Execute command failed %r: <%s>-<%s>" % (returncode, stdout_text, stderr_text))
					return flask.jsonify(dict(success=False, msg=str(stdout_text)))
			except:
				self.logger.exception("Could not execute command due to unknown error")
				return flask.jsonify(dict(success=False, msg=str('error!!!')))

		return flask.make_response("Unknown command", 400)

	def on_api_get(self, request):
		self.logger.warn("Invoking <on_api_get>")

	##~~ SettingsPlugin API

	def on_settings_load(self):
		self.logger.warn("Invoking <on_settings_load>")
		return dict(
			shell=""
		)


	def on_settings_save(self, data):
		self.logger.warn("Invoking <on_settings_save>")
	#~~ EventPlugin API

	def on_event(self, event, payload):
		self.logger.warn("Invoking <on_event>")

__plugin_name__ = "AndroidConnect"
__plugin_description__ = "Setup Android Connection within Octoprint"
__plugin_implementations__ = [AndroidConnectPlugin()]
