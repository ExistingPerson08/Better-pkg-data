def register(command_handlers, hooks, setup_functions=None, package_groups_extensions=None, custom_json_handlers=None):
    import shutil
    import os
    import subprocess

    def print_status(message, status="info"):
        """Barevný výpis stavových zpráv"""
        colors = Colors()
        if status == "info":
            print(f"{colors.BCyan}ℹ {message}{colors.NC}")
        elif status == "success":
            print(f"{colors.BGreen}✓ {message}{colors.NC}")
        elif status == "warning":
            print(f"{colors.BYellow}⚠ {message}{colors.NC}")
        elif status == "error":
            print(f"{colors.BRed}✗ {message}{colors.NC}")
    
    def upgrade_pip(args):
        for pip_cmd in ["pip", "pip3"]:
            if shutil.which(pip_cmd):
                print_status(f"Upgrading {pip_cmd} packages...", "info")
                try:
                    # Get list of outdated packages
                    result = subprocess.run([pip_cmd, "list", "--outdated", "--format=freeze"], capture_output=True, text=True)
                    pkgs = [line.split('==')[0] for line in result.stdout.splitlines() if '==' in line]
                    if pkgs:
                        subprocess.run([pip_cmd, "install", "--upgrade"] + pkgs, check=True)
                        print_status(f"{pip_cmd} packages upgraded.", "success")
                    else:
                        print_status(f"No {pip_cmd} packages to upgrade.", "info")
                except Exception as e:
                    print_status(f"Error upgrading {pip_cmd} packages: {e}", "error")

    hooks["upgrade-plugin"].append(upgrade_pip)
