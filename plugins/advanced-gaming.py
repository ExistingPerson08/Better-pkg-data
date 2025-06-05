# ~/.local/share/better-tools/plugins/advanced-gaming.py
def register(command_handlers, hooks, setup_functions=None, package_groups_extensions=None):
    # 1. Rozšíření skupin
    def extend_groups(groups):
        groups["advanced-gaming"] = {
            "packages": {
                "vkbasalt": ["dnf", "pacman", "yay"],
                "gamemode": ["apt", "dnf", "pacman", "yay"],
            },
            "flatpak": {
                "com.heroicgameslauncher.hgl": "flatpak"
            }
        }
        # Rozšíří existující skupinu
        if "gaming" in groups:
            groups["gaming"]["packages"]["vkbasalt"] = ["dnf", "pacman", "yay"]
    if package_groups_extensions is not None:
        package_groups_extensions.append(extend_groups)

    # 2. Registrace setup funkce
    def advanced_gaming_setup():
        print("\033[1;34m[advanced-gaming]\033[0m Spouštím setup: advanced-gaming")
        # Získání skupiny z get_package_groups
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
        setup_functions["advanced-gaming"] = advanced_gaming_setup
