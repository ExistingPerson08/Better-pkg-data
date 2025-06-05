def register(command_handlers, hooks, setup_functions=None, package_groups_extensions=None, custom_json_handlers=None):
    import os
    import urllib.request

    def install_plugins(plugin_list):
        plugins_dir = os.path.expanduser("~/.local/share/better-tools/plugins/")
        os.makedirs(plugins_dir, exist_ok=True)
        for plugin_name in plugin_list:
            plugin_url = f"https://raw.githubusercontent.com/ExistingPerson08/Better-pkg-data/main/plugins/{plugin_name}.py"
            plugin_path = os.path.join(plugins_dir, f"{plugin_name}.py")
            try:
                print(f"Installing plugin '{plugin_name}'...")
                urllib.request.urlretrieve(plugin_url, plugin_path)
                print(f"Plugin '{plugin_name}' installed to {plugin_path}.")
            except Exception as e:
                print(f"Failed to install plugin '{plugin_name}': {e}")

    if custom_json_handlers is not None:
        # Umožní v JSON sekci např. "plugins": ["cache-cleaner", "advanced-gaming"]
        custom_json_handlers["plugins"] = install_plugins
