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

    def upgrade_extensions(args):
        if shutil.which("code"):
            print_status("Upgrading VSCode extensions...", "info")
            try:
                # There is no direct upgrade command; reinstall all extensions to force update
                result = subprocess.run("code --list-extensions", shell=True, capture_output=True, text=True)
                extensions = result.stdout.strip().splitlines()
                for ext in extensions:
                    subprocess.run(f"code --install-extension {ext} --force", shell=True, check=True)
                print_status("VSCode extensions upgraded.", "success")
            except Exception as e:
                print_status(f"Error upgrading VSCode extensions: {e}", "error")

        if shutil.which("gnome-extensions"):
            import zipfile
            import tempfile

            print_status("Upgrading GNOME Shell extensions...", "info")
            try:
                # Try to update extensions using gnome-extensions CLI (GNOME 45+)
                result = subprocess.run("gnome-extensions upgrade --all", shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print_status("GNOME Shell extensions upgraded using gnome-extensions CLI.", "success")
                    return
                else:
                    # Fallback: update extensions manually from extensions.gnome.org
                    print_status("gnome-extensions CLI upgrade failed or not supported, trying manual update...", "warning")
            except Exception:
                # Fallback if gnome-extensions upgrade is not available
                pass

            try:
                # Manual update: download and install latest versions from extensions.gnome.org
                import urllib.request
                import json

                # Get list of installed extensions and their UUIDs
                result = subprocess.run("gnome-extensions list", shell=True, capture_output=True, text=True)
                extensions = result.stdout.strip().splitlines()

                # Get GNOME Shell version
                shell_ver_result = subprocess.run("gnome-shell --version", shell=True, capture_output=True, text=True)
                shell_ver = shell_ver_result.stdout.strip().split()[-1]

                for ext in extensions:
                    # Skip system extensions (those not in ~/.local/share/gnome-shell/extensions)
                    user_ext_dir = os.path.expanduser("~/.local/share/gnome-shell/extensions")
                    ext_path = os.path.join(user_ext_dir, ext)
                    if not os.path.isdir(ext_path):
                        continue  # This is a system extension

                    # Get extension info (including UUID)
                    info_result = subprocess.run(f"gnome-extensions info {ext}", shell=True, capture_output=True, text=True)
                    uuid = None
                    for line in info_result.stdout.splitlines():
                        if line.startswith("uuid:"):
                            uuid = line.split(":", 1)[1].strip()
                            break
                    if not uuid:
                        uuid = ext

                    # Query extensions.gnome.org for latest version
                    url = f"https://extensions.gnome.org/extension-info/?uuid={uuid}&shell_version={shell_ver}"
                    try:
                        with urllib.request.urlopen(url, timeout=5) as resp:
                            data = json.load(resp)
                            download_url = "https://extensions.gnome.org" + data["download_url"]
                            # Download the extension zip
                            with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmpfile:
                                urllib.request.urlretrieve(download_url, tmpfile.name)
                                # Install the extension
                                subprocess.run(f"gnome-extensions install --force {tmpfile.name}", shell=True, check=True)
                                os.unlink(tmpfile.name)
                            print_status(f"Extension '{uuid}' updated.", "success")
                    except Exception as e:
                        print_status(f"Could not update extension '{uuid}': {e}", "warning")
                print_status("GNOME Shell extensions update finished.", "success")
            except Exception as e:
                print_status(f"Error upgrading GNOME extensions: {e}", "error")

    hooks["upgrade-plugin"].append(upgrade_extensions)
