def register(command_handlers, hooks, setup_functions=None, package_groups_extensions=None):
    # Přidání nové skupiny do get_package_groups přes extender
    def extend_groups(groups):
        groups["advanced-gaming"] = {
            "packages": {
                "vkbasalt": ["dnf", "pacman", "yay"],
                "gamemode": ["apt", "dnf", "pacman", "yay"],
                "protontricks": ["apt", "dnf", "pacman", "yay"],
                "mangohud": ["apt", "dnf", "pacman", "yay"],
                "goverlay": ["dnf", "pacman", "yay"],
                "corectrl": ["dnf", "pacman", "yay"],
                "wine": ["apt", "dnf", "pacman", "yay"],
                "winetricks": ["apt", "dnf", "pacman", "yay"],
                "steam-devices": ["pacman", "yay"],
                "steam-tui": ["yay"],
                "gamescope": ["dnf", "pacman", "yay"],
                "vkmark": ["dnf", "pacman", "yay"],
            },
            "flatpak": {
                "com.usebottles.bottles": "flatpak",
                "com.heroicgameslauncher.hgl": "flatpak",
                "org.prismlauncher.PrismLauncher": "flatpak"
            }
        }
        # Rozšíří existující skupinu gaming
        if "gaming" in groups:
            groups["gaming"]["packages"]["vkbasalt"] = ["dnf", "pacman", "yay"]

    if package_groups_extensions is not None:
        package_groups_extensions.append(extend_groups)

    # Přidání setup funkce pro advanced-gaming-tools
    def advanced_gaming_tools_setup():
        print("\033[1;34m[advanced-gaming]\033[0m Spouštím setup: advanced-gaming-tools")
        # Předpokládá, že install_packages je globálně dostupná funkce v hlavním skriptu
        try:
            from better_pkg import install_packages  # Pokud by byl projekt jako modul
        except ImportError:
            # Pokud není jako modul, použij volání přes SETUP_FUNCTIONS
            pass
        # Většina implementací má install_packages dostupné v hlavním skriptu, takže stačí:
        # Získání skupin přes get_package_groups
        import sys
        main_mod = sys.modules["__main__"]
        get_package_groups = getattr(main_mod, "get_package_groups", None)
        install_packages = getattr(main_mod, "install_packages", None)
        if get_package_groups and install_packages:
            groups = get_package_groups()
            group = groups.get("advanced-gaming")
            if group:
                install_packages(group["packages"], group.get("flatpak"))
            else:
                print("advanced-gaming group not found.")
        else:
            print("Cannot access install_packages or get_package_groups from main script.")

    if setup_functions is not None:
        setup_functions["advanced-gaming-tools"] = advanced_gaming_tools_setup
