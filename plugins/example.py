def register(command_handlers, hooks, setup_functions=None, package_groups_extensions=None, custom_json_handlers=None):
    def my_command(args):
        print("example_command: Custom command executed!")
        
    import sys
    main_mod = sys.modules["__main__"]
    plugin_commands = getattr(main_mod, "PLUGIN_COMMANDS", None)
    if plugin_commands is not None:
        plugin_commands.append(("example", my_command, "Example command description"))
