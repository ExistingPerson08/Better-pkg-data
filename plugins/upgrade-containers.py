def register(command_handlers, hooks, setup_functions=None, package_groups_extensions=None, custom_json_handlers=None):
    import shutil
    import os
    import subprocess

    def upgrade_containers(args):
        if shutil.which("docker"):
            print("Upgrading Docker containers...", "info")
            try:
                subprocess.run("docker system prune -af", shell=True, check=True)
                result = subprocess.run("docker ps -q", shell=True, capture_output=True, text=True)
                container_ids = result.stdout.splitlines()
                for cid in container_ids:
                    subprocess.run(f"docker restart {cid}", shell=True)
                print("Docker containers upgraded (images pruned, containers restarted).", "success")
            except Exception as e:
                print(f"Error upgrading Docker containers: {e}", "error")

        if shutil.which("podman"):
            print("Upgrading Podman containers...", "info")
            try:
                subprocess.run("podman system prune -af", shell=True, check=True)
                result = subprocess.run("podman ps -q", shell=True, capture_output=True, text=True)
                container_ids = result.stdout.splitlines()
                for cid in container_ids:
                    subprocess.run(f"podman restart {cid}", shell=True)
                print("Podman containers upgraded (images pruned, containers restarted).", "success")
            except Exception as e:
                print(f"Error upgrading Podman containers: {e}", "error")

    hooks["upgrade-plugin"].append(upgrade_containers)
