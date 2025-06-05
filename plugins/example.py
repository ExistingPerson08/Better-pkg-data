# ~/.local/share/better-tools/plugins/example.py
def register(command_handlers, hooks=None):
    def my_pre_upgrade(args):
        print("Plugin: I do something during upgrade!")
    if hooks:
        hooks["upgrade-plugin"].append(my_pre_upgrade)
