def register(command_handlers, hooks, setup_functions=None, package_groups_extensions=None, custom_json_handlers=None):
    def my_setup():
        print("Hello from example_setup plugin! This is a custom setup.")
    if setup_functions is not None:
        setup_functions["example-setup"] = my_setup
