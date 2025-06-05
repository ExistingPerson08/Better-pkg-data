# ~/.local/share/better-tools/plugins/advanced-gaming.py
def register(command_handlers, hooks, setup_functions):
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
    # Zaregistruj extender
    import sys
    sys.modules["better-pkg"].PACKAGE_GROUPS_EXTENSIONS.append(extend_groups)
