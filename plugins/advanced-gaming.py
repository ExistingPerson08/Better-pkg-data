def register(command_handlers, hooks, setup_functions=None, package_groups_extensions=None):
    def advanced_gaming_tools_setup():
        print("\033[1;34m[advanced-gaming-tools]\033[0m Running setup: advanced-gaming-tools")
        import sys
        main_mod = sys.modules["__main__"]
        install_packages = getattr(main_mod, "install_packages", None)
        if install_packages:
            # Define tools directly here (or extend via package_groups_extensions if you want)
            packages = {
                "protontricks": ["apt", "dnf", "pacman", "yay"],
                "gamemode": ["apt", "dnf", "pacman", "yay"],
                "vkbasalt": ["dnf", "pacman", "yay"],
                "mangohud": ["apt", "dnf", "pacman", "yay"],
                "goverlay": ["dnf", "pacman", "yay"],
                "corectrl": ["dnf", "pacman", "yay"],
                "wine": ["apt", "dnf", "pacman", "yay"],
                "winetricks": ["apt", "dnf", "pacman", "yay"],
                "gamescope": ["dnf", "pacman", "yay"],
            }
            flatpak_packages = {
                "com.usebottles.bottles": "flatpak",
                "com.heroicgameslauncher.hgl": "flatpak",
                "org.prismlauncher.PrismLauncher": "flatpak"
            }
            install_packages(packages, flatpak_packages)
        else:
            print("Cannot access install_packages from main script.")

    if setup_functions is not None:
        setup_functions["advanced-gaming-tools"] = advanced_gaming_tools_setup
