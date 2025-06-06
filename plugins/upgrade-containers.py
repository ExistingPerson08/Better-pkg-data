def register(command_handlers, hooks, setup_functions=None, package_groups_extensions=None, custom_json_handlers=None):
    import shutil
    import os
    import subprocess

    class Colors:
        def __init__(self):
            self.use_color = "NO_COLOR" not in os.environ
            if self.use_color:
                self.NC = '\033[0m'
                self.BGreen = '\033[1;32m'
                self.BCyan = '\033[1;36m'
                self.BYellow = '\033[1;33m'
                self.BPurple = '\033[1;35m'
                self.BRed = '\033[1;31m'
                self.BWhite = '\033[1;37m'
                self.c1 = '\u001b[38;5;104m'  # light purple
                self.c2 = '\u001b[0m'         # white/reset
                self.c3 = '\u001b[38;5;55m'   # dark purple
                self.c4 = '\u001b[38;5;98m'   # medium purple
            else:
                self.NC = self.BGreen = self.BCyan = self.BYellow = ''
                self.BPurple = self.BRed = self.BWhite = ''
                self.c1 = self.c2 = self.c3 = self.c4 = ''

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

    def upgrade_containers(args):
        if shutil.which("docker"):
            print_status("Upgrading Docker containers...", "info")
            try:
                subprocess.run("docker system prune -af", shell=True, check=True)
                result = subprocess.run("docker ps -q", shell=True, capture_output=True, text=True)
                container_ids = result.stdout.splitlines()
                for cid in container_ids:
                    subprocess.run(f"docker restart {cid}", shell=True)
                print_status("Docker containers upgraded (images pruned, containers restarted).", "success")
            except Exception as e:
                print_status(f"Error upgrading Docker containers: {e}", "error")

        if shutil.which("podman"):
            print_status("Upgrading Podman containers...", "info")
            try:
                subprocess.run("podman system prune -af", shell=True, check=True)
                result = subprocess.run("podman ps -q", shell=True, capture_output=True, text=True)
                container_ids = result.stdout.splitlines()
                for cid in container_ids:
                    subprocess.run(f"podman restart {cid}", shell=True)
                print_status("Podman containers upgraded (images pruned, containers restarted).", "success")
            except Exception as e:
                print_status(f"Error upgrading Podman containers: {e}", "error")

    hooks["upgrade-plugin"].append(upgrade_containers)
