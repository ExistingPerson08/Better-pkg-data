def register(command_handlers, hooks, setup_functions, package_groups_extensions):
    def extend_groups(groups):
        # Přidá novou skupinu
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
    package_groups_extensions.append(extend_groups)
