$(function() {
    function AndroidConnectViewModel(parameters) {
        var self = this;

        self.loginState = parameters[0];
        self.settingsViewModel = parameters[1];

        self.execActive = ko.observable(false);
        self.execResult = ko.observable(false);
        self.execSuccessful = ko.observable(false);
        self.execMessage = ko.observable();

        // initialize list helper
        self.listHelper = new ItemListHelper(
            "android_connectHosts",
            {
                "name": function(a, b) {
                    // sorts ascending
                    if (a["name"].toLocaleLowerCase() < b["name"].toLocaleLowerCase()) return -1;
                    if (a["name"].toLocaleLowerCase() > b["name"].toLocaleLowerCase()) return 1;
                    return 0;
                }
            },
            {},
            "name",
            [],
            [],
            10
        );

        self.chooseInstance = function(data) {
            self.settings.plugins.android_connect.shell(data.shell);
        };

        self.execConfiguration = function() {
            self.execActive(true);
            self.execResult(false);
            self.execSuccessful(false);
            self.execMessage("");

            var shell = self.settings.plugins.android_connect.shell();

            var payload = {
                command: "execute",
                shell: shell
            };

            $.ajax({
                url: API_BASEURL + "plugin/android_connect",
                type: "POST",
                dataType: "json",
                data: JSON.stringify(payload),
                contentType: "application/json; charset=UTF-8",
                success: function(response) {
                    self.execResult(true);
                    self.execSuccessful(false);
                    if (response.hasOwnProperty("msg")) {
                        self.execMessage(response.msg.concat(" <", response.success.toString(), ">"));
                    } else {
                        self.execMessage(undefined);
                    }
                },
                complete: function() {
                    self.execActive(false);
                }
            });
        };

        self.onBeforeBinding = function() {
            self.settings = self.settingsViewModel.settings;
        };

        self.onSettingsShown = function() {
        };

    }

    // view model class, parameters for constructor, container to bind to
    ADDITIONAL_VIEWMODELS.push([AndroidConnectViewModel, ["loginStateViewModel", "settingsViewModel"], document.getElementById("settings_plugin_android_connect_dialog")]);
});