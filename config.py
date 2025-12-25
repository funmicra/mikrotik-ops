import os
from dotenv import load_dotenv
from typing import Optional, Any

load_dotenv()


class ConfigError(Exception):
    """Raised when a required environment variable is missing."""
    pass


def get_env(
    key: str,
    required: bool = True,
    default: Optional[Any] = None
) -> Optional[str]:
    """
    Fetches an environment variable with optional default and required checks.

    Args:
        key (str): Environment variable name.
        required (bool): If True, raises ConfigError if missing.
        default (Optional[Any]): Default value if env var is not set.

    Returns:
        Optional[str]: The environment variable value.
    """
    value = os.getenv(key, default)
    if required and value is None:
        raise ConfigError(f"Missing required environment variable: {key}")
    return value


def get_env_int(key: str, default: Optional[int] = None) -> int:
    """
    Fetches an integer environment variable with a default.

    Args:
        key (str): Environment variable name.
        default (Optional[int]): Default value if env var is not set.

    Returns:
        int: Converted integer value.
    """
    val_str = get_env(key, required=(default is None), default=str(default))
    try:
        return int(val_str)  # type: ignore
    except (ValueError, TypeError):
        raise ConfigError(f"Invalid integer value for {key}: {val_str}")


def get_env_bool(key: str, default: bool = False) -> bool:
    """
    Fetches a boolean environment variable.

    Args:
        key (str): Environment variable name.
        default (bool): Default if env var not set.

    Returns:
        bool: True/False based on env var.
    """
    val_str = get_env(key, required=False, default=str(default))
    return val_str.strip().lower() in ("1", "true", "yes", "on")


# ─────────────────────────────
# SSH / Authentication
# ─────────────────────────────

MT_USERNAME = get_env("MT_USERNAME")

# Optional: password-based SSH
MT_PASSWORD = get_env("MT_PASSWORD", required=False)

# Optional: key-based SSH (preferred)
MT_SSH_KEY = get_env("MT_SSH_KEY", required=False)

MT_SSH_PORT = int(get_env("MT_SSH_PORT", default=22))


# ─────────────────────────────
# Runtime behavior
# ─────────────────────────────

DRY_RUN = get_env("DRY_RUN", default="true").lower() == "true"
LOG_LEVEL = get_env("LOG_LEVEL", default="INFO")


# ─────────────────────────────
# Router inventory
# ─────────────────────────────

ROUTER_NAMES = [
    r.strip() for r in get_env("MT_ROUTERS").split(",")
]

ROUTERS = {}
for name in ROUTER_NAMES:
    ip = get_env(f"MT_ROUTER_{name.upper()}")
    ROUTERS[name] = ip
