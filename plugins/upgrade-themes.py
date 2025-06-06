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

    def upgrade_themes(args):
        def upgrade_kde_themes():
            if shutil.which("plasma-discover"):
                print_status("Upgrading KDE themes and add-ons...", "info")
                try:
                    subprocess.run("plasma-discover --mode update", shell=True, check=True)
                    print_status("KDE themes/add-ons upgraded.", "success")
                except Exception as e:
                    print_status(f"Error upgrading KDE themes/add-ons: {e}", "error")

        def upgrade_ohmyzsh():
            if shutil.which("zsh") and os.path.exists(os.path.expanduser("~/.oh-my-zsh")):
                print_status("Upgrading Oh My Zsh...", "info")
                try:
                    subprocess.run("omz update", shell=True, check=True)
                    print_status("Oh My Zsh upgraded.", "success")
                except Exception as e:
                    print_status(f"Error upgrading Oh My Zsh: {e}", "error")

        def upgrade_npm_global():
            if shutil.which("npm"):
                print_status("Upgrading global npm packages...", "info")
                try:
                    subprocess.run("npm update -g", shell=True, check=True)
                    print_status("Global npm packages upgraded.", "success")
                except Exception as e:
                    print_status(f"Error upgrading global npm packages: {e}", "error")

        def upgrade_themes_icons():
            print_status("Upgrading user themes/icons...", "info")
            # oh-my-posh
            if shutil.which("oh-my-posh"):
                try:
                    subprocess.run("oh-my-posh update", shell=True, check=True)
                    print_status("oh-my-posh upgraded.", "success")
                except Exception as e:
                    print_status(f"Error upgrading oh-my-posh: {e}", "error")
            # GNOME themes
            themes_dir = os.path.expanduser("~/.themes")
            if os.path.isdir(themes_dir):
                try:
                    for theme in os.listdir(themes_dir):
                        theme_path = os.path.join(themes_dir, theme)
                        if os.path.isdir(theme_path) and os.path.isdir(os.path.join(theme_path, ".git")):
                            subprocess.run(f"git -C '{theme_path}' pull", shell=True, check=True)
                            print_status(f"Theme '{theme}' updated from git.", "success")
                except Exception as e:
                    print_status(f"Error upgrading GNOME themes: {e}", "error")
            # GNOME icons
            icons_dir = os.path.expanduser("~/.icons")
            if os.path.isdir(icons_dir):
                try:
                    for icon in os.listdir(icons_dir):
                        icon_path = os.path.join(icons_dir, icon)
                        if os.path.isdir(icon_path) and os.path.isdir(os.path.join(icon_path, ".git")):
                            subprocess.run(f"git -C '{icon_path}' pull", shell=True, check=True)
                            print_status(f"Icon theme '{icon}' updated from git.", "success")
                except Exception as e:
                    print_status(f"Error upgrading GNOME icon themes: {e}", "error")

        def upgrade_ohmyfish():
            if shutil.which("fish") and os.path.exists(os.path.expanduser("~/.local/share/omf")):
                print_status("Upgrading Oh My Fish...", "info")
                try:
                    subprocess.run("fish -c 'omf update'", shell=True, check=True)
                    print_status("Oh My Fish upgraded.", "success")
                except Exception as e:
                    print_status(f"Error upgrading Oh My Fish: {e}", "error")

        # Spuštění všech upgrade funkcí
        upgrade_kde_themes()
        upgrade_ohmyzsh()
        upgrade_npm_global()
        upgrade_themes_icons()
        upgrade_ohmyfish()

    hooks["upgrade-plugin"].append(upgrade_themes)
