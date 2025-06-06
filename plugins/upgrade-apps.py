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

    def upgrade_apps(args):
        print_status("Upgrading GitHub applications...", "info")
        
        # Add localized Applications folders (e.g. ~/Aplikace, ~/Applikationen, etc.)
        localized_app_dirs = [
            os.path.expanduser("~/Applications"),
            os.path.expanduser("~/Aplikace"),
            os.path.expanduser("~/Applikationen"),
            os.path.expanduser("~/Aplicaciones"),
            os.path.expanduser("~/Applicazioni"),
            os.path.expanduser("~/Aplikacje"),
            os.path.expanduser("~/Aplikaatiot"),
            os.path.expanduser("~/Aplikácie"),
            os.path.expanduser("~/Aplikacije"),
            os.path.expanduser("~/Aplikacijos"),
            os.path.expanduser("~/.local/bin"),
        ]

        checked = set()

        # Git repositories
        for app_dir in localized_app_dirs:
            if app_dir in checked:
                continue
            checked.add(app_dir)
            if os.path.isdir(app_dir):
                for fname in os.listdir(app_dir):
                    fpath = os.path.join(app_dir, fname)
                    if os.path.isdir(fpath) and os.path.isdir(os.path.join(fpath, ".git")):
                        try:
                            subprocess.run(f"git -C '{fpath}' pull", shell=True, check=True)
                            print_status("fGitHub app '{fname}' updated from git.", "success")
                        except Exception as e:
                            print_status("fError upgrading GitHub app '{fname}': {e}", "error")

        # AppImages
        checked = set()
        for app_dir in localized_app_dirs:
            if app_dir in checked:
                continue
            checked.add(app_dir)
            if os.path.isdir(app_dir):
                for fname in os.listdir(app_dir):
                    fpath = os.path.join(app_dir, fname)
                    if os.path.isfile(fpath) and fpath.endswith(".AppImage"):
                        updated = False
                        # Try AppImageUpdate
                        if shutil.which("AppImageUpdate"):
                            try:
                                subprocess.run(["AppImageUpdate", fpath], check=True)
                                print_status("fAppImage '{fname}' updated with AppImageUpdate.", "success")
                                updated = True
                            except Exception as e:
                                print_status("fError updating AppImage '{fname}' with AppImageUpdate: {e}", "error")
                        # Try Gearlever (Flatpak)
                        if not updated and shutil.which("flatpak") and shutil.which("gearlever"):
                            try:
                                subprocess.run([
                                    "flatpak", "run", "io.github.prateekmedia.gearlever",
                                    "--update", fpath
                                ], check=True)
                                print_status("fAppImage '{fname}' updated with Gearlever.", "success")
                                updated = True
                            except Exception as e:
                                print_status("fError updating AppImage '{fname}' with Gearlever: {e}", "error")
                        # Try appimaged (if running)
                        if not updated and shutil.which("appimaged"):
                            try:
                                os.utime(fpath, None)
                                print_status("fAppImage '{fname}' touched for appimaged rescan.", "info")
                                updated = True
                            except Exception as e:
                                print_status("fError triggering appimaged for '{fname}': {e}", "error")
                        if not updated:
                            print_status("fNo supported AppImage updater found for '{fname}'.", "warning")

    hooks["upgrade-plugin"].append(upgrade_apps)
