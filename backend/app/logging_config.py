import logging
import logging.handlers
import os


def setup_logging() -> None:
    """
    Configure the root logger once at application startup.
    Writes to the console and to a rotating file at app/logs/app.log.
    Calling this more than once is safe — handlers are only added if none exist.
    """
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # Guard: avoid duplicate handlers when modules are reloaded (e.g. pytest)
    if root.handlers:
        return

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root.addHandler(console)

    # 5 MB per file, keep the 3 most recent rotations
    rotating = logging.handlers.RotatingFileHandler(
        os.path.join(logs_dir, "app.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    rotating.setFormatter(formatter)
    root.addHandler(rotating)
