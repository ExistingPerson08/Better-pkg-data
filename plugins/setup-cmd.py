def register(command_handlers, hooks, setup_functions=None, package_groups_extensions=None, custom_json_handlers=None):
    import subprocess

    def run_commands(commands):
        """
        Run shell commands from the JSON section "commands": ["echo hello", "ls -l"]
        """
        if not isinstance(commands, list):
            print("[commands_from_json] 'commands' section must be a list of strings.")
            return
        for cmd in commands:
            print(f"[commands_from_json] Running: {cmd}")
            try:
                subprocess.run(cmd, shell=True, check=True)
            except Exception as e:
                print(f"[commands_from_json] Error running '{cmd}': {e}")

    if custom_json_handlers is not None:
        custom_json_handlers["commands"] = run_commands
