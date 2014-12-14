# coding=utf-8
from __future__ import absolute_import

__author__ = "Extensio <info@extensio.ru>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2014 Extensio 3D Console - Released under terms of the AGPLv3 License"

import flask
import logging

import octoprint.plugin
import octoprint.events
from time import sleep

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

	def checkWifiMode(self):
		if self.execute_command("service call wifi 29").count("00000000 0000000d") > 0:
			return "AP"
		return "Client"

	#~~ TemplatePlugin API
	def get_template_vars(self):
		wifiMode = self.checkWifiMode()
		return dict(
			_settings_menu_entry="Configure Wi-Fi",
			_config_wifi_mode=wifiMode
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
			wifiConnect=["ssid", "password"],
			startAP=["ssid", "password"]
		)

	def execute_command(self, command_str):
		import sarge
		self.logger.warn("Executing command: %s" % command_str)
		try:
			p = sarge.run(command_str, stdout=sarge.Capture(), stderr=sarge.Capture())
			returncode = p.returncode
			stderr_text = p.stderr.text
			stdout_text = p.stdout.text
			if returncode != 0:
				self.logger.warn("Executed command success %r: <%s>-<%s>" % (returncode, stdout_text, stderr_text))
				raise Exception(stdout_text)
			self.logger.warn("Success. Out:<%s> Error:<%s>" % (stdout_text, stderr_text))
			return stdout_text
		except:
			self.logger.exception("Could not execute command due to unknown error")
			raise Exception('error!!!')


	def on_api_command(self, command, data):
		if command == "wifiConnect":
			self.logger.warn("Command wifiConnect is invoked")
			ssid = data["ssid"]
			password = data["password"]
			out = ''
			try:
				out += self.execute_command("service call wifi 28 i32 0 i32 0")
				out += self.execute_command("service call wifi 13 i32 1")
				for i in range (0,30):
					if self.execute_command("service call wifi 14").count("00000000 00000003") > 0:
						break
					sleep(1)
				out += self.execute_command("service call wifi 2 i32 1 i32 -1  i32 0 i32 0 s16 \\\"" + ssid + "\\\" i32 -1 s16 \\\"" + password + "\\\" i32 -1 i32 -1 i32 -1 i32 -1 i32 0 i32 1 i32 0 i32 1 i32 1 i32 2 i32 0 i32 1 i32 0 i32 2 i32 1 i32 2 i32 4 i32 0 i32 1 i32 2 i32 3 i32 -1 i32 -1 i32 -1 i32 -1 i32 -1 i32 -1 i32 1 i32 48 i32 -1 i32 -1 i32 -1 s16 DHCP s16 NONE s16 android.net.LinkProperties i32 -1 i32 0 i32 0 i32 0 i32 0")
				out += self.execute_command("service call wifi 19")
				out += self.execute_command("service call wifi 32")
			except Exception as e:
				flask.jsonify(dict(success=False, msg=str(e.args)))
			self.logger.warn("Command wifiConnect output is %s", out)
			return flask.jsonify(dict(success=True, msg=str("")))
		if command == "startAP":
			self.logger.warn("Command startAP is invoked")
			ssid = data["ssid"]
			password = data["password"]
			out = ''
			try:
				out += self.execute_command("service call wifi 13 i32 0")
				out += self.execute_command("service call wifi 28 i32 0 i32 1")
			except Exception as e:
				flask.jsonify(dict(success=False, msg=str(e.args)))
			self.logger.warn("Command startAP output is %s", out)
			return flask.jsonify(dict(success=True, msg=str("")))

		return flask.make_response("Unknown command", 400)

	def on_api_get(self, request):
		self.logger.warn("Invoking <on_api_get>")

	##~~ SettingsPlugin API

	def on_settings_load(self):
		self.logger.warn("Invoking <on_settings_load>")
		return dict(
			ssid="",
			password=""
		)


	def on_settings_save(self, data):
		self.logger.warn("Invoking <on_settings_save>")
	#~~ EventPlugin API

	def on_event(self, event, payload):
		self.logger.warn("Invoking <on_event>")

__plugin_name__ = "AndroidConnect"
__plugin_description__ = "Setup Android Connection within Octoprint"
__plugin_implementations__ = [AndroidConnectPlugin()]
