def register(command_handlers, hooks, setup_functions=None, package_groups_extensions=None, custom_json_handlers=None):
    def my_command(args):
        print("example_command: Custom command executed!")
    command_handlers["example"] = my_command
