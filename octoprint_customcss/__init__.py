# coding=utf-8
from __future__ import absolute_import

from tempfile import NamedTemporaryFile
from os import path, unlink

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

class CustomCSSPlugin(octoprint.plugin.ShutdownPlugin,
                      octoprint.plugin.SettingsPlugin,
                      octoprint.plugin.AssetPlugin,
                      octoprint.plugin.TemplatePlugin):

    def __init__(self, filename=None):
        super( CustomCSSPlugin, self ).__init__()
        self.cssfile = NamedTemporaryFile(dir=path.join(path.dirname(path.realpath(__file__)), 'static/css'), prefix='usercss', suffix='.css', delete=False)

    def on_shutdown(self):
        unlink(self.cssfile.name)
        self._logger.info("unlinking {cssfile}".format(cssfile = self.cssfile.name))

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            custom_css="/* Place some custom CSS here, then save and refresh! */"
        )

    def on_settings_save(self, data):
        old_css = self._settings.get(["custom_css"])
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        new_css = self._settings.get(["custom_css"])
        if old_css != new_css:
            self.write_assets_file()
            self._logger.info("custom_css changed, UI reload required")

    ##~~ AssetPlugin mixin

    def write_assets_file(self):
        custom_css = self._settings.get(["custom_css"])
        self.cssfile.file.seek(0)
        self.cssfile.file.truncate()
        self.cssfile.file.write("/* BEGIN CUSTOM CSS */\n{custom_css}\n/* END CUSTOM CSS */".format(custom_css = custom_css))
        self.cssfile.file.flush()
        return self.cssfile.name

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        self.write_assets_file()
        return dict(
            css=[self.cssfile.name, "css/customcss.css"],
        )

    ##~~ SettingsPlugin mixin

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
        # for details.
        return dict(
            customcss=dict(
                displayName="Customcss Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="cryptk",
                repo="OctoPrint_CustomCSS",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/cryptk/OctoPrint_CustomCSS/archive/{target_version}.zip"
            )
        )


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = CustomCSSPlugin()

#   global __plugin_hooks__
#   __plugin_hooks__ = {
#       "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
#   }

