def register(command_handlers, hooks, setup_functions=None, package_groups_extensions=None):
    import shutil
    import os
    import subprocess

    def deep_cache_cleanup(args):
        print("\033[1;36m[cache-cleaner]\033[0m Removing deep system/user cache...")
        # Systémové cache adresáře
        cache_dirs = [
            "/var/cache",
            "/var/tmp",
            "/var/log/journal",
            "/var/lib/flatpak/cache",
            "/var/lib/snapd/cache",
            "/var/lib/pacman/sync",
            "/var/cache/pacman/pkg",
            "/var/cache/apt/archives",
            "/var/cache/dnf",
            "/var/cache/zypp/packages",
        ]
        # Uživatelské cache adresáře
        user_cache_dirs = [
            os.path.expanduser("~/.cache"),
            os.path.expanduser("~/.npm/_cacache"),
            os.path.expanduser("~/.config/google-chrome/Default/Cache"),
            os.path.expanduser("~/.config/chromium/Default/Cache"),
            os.path.expanduser("~/.var/app"),
        ]

        # Smazání obsahu adresářů (ne samotných adresářů)
        for d in cache_dirs + user_cache_dirs:
            if os.path.exists(d):
                try:
                    for entry in os.listdir(d):
                        path = os.path.join(d, entry)
                        if os.path.isdir(path):
                            shutil.rmtree(path, ignore_errors=True)
                        else:
                            try:
                                os.remove(path)
                            except Exception:
                                pass
                    print(f"\033[1;32m✓ Cleared: {d}\033[0m")
                except Exception as e:
                    print(f"\033[1;31m✗ Error cleaning {d}: {e}\033[0m")

        # Vyčištění docker a podman cache (pokud jsou k dispozici)
        for tool in ["docker", "podman"]:
            if shutil.which(tool):
                try:
                    subprocess.run([tool, "system", "prune", "-af"], check=False)
                    print(f"\033[1;32m✓ {tool} system prune done\033[0m")
                except Exception as e:
                    print(f"\033[1;31m✗ Error running {tool} prune: {e}\033[0m")

        print("\033[1;36m[cache-cleaner]\033[0m Deep cache cleanup finished.")

    # Přidej plugin do cleanup hooku
    hooks["cleanup-plugin"].append(deep_cache_cleanup)
