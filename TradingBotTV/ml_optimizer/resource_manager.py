import sys


def configure_resources() -> None:
    """Limit memory usage on Unix-like systems."""
    if sys.platform == "win32":
        print(
            "[INFO] Ograniczenie pamieci nie jest dostepne w systemie "
            "Windows. Pomijam konfiguracje zasobow."
        )
        return

    import resource  # only available on Unix/Linux/macOS

    gigabyte = 1024 * 1024 * 1024
    new_limit = 16 * gigabyte
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (new_limit, hard))
