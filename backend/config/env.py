import os
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def get_env(
    name: str,
    *,
    cast: Callable[[str], T] = str,
    default: T | None = None,
    required: bool = False,
) -> T:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        if required and default is None:
            raise RuntimeError(f"Environment variable {name} is required")
        return default  # type: ignore[return-value]

    try:
        return cast(raw)
    except Exception as exc:
        raise RuntimeError(f"Environment variable {name} has invalid value") from exc


def get_bool(name: str, *, default: bool | None = None, required: bool = False) -> bool:
    def _cast(v: str) -> bool:
        v_norm = v.strip().lower()
        if v_norm in {"1", "true", "yes", "y", "on"}:
            return True
        if v_norm in {"0", "false", "no", "n", "off"}:
            return False
        raise ValueError

    return get_env(name, cast=_cast, default=default, required=required)


def get_csv(
    name: str, *, default: list[str] | None = None, required: bool = False
) -> list[str]:
    def _cast(v: str) -> list[str]:
        parts = [p.strip() for p in v.split(",")]
        return [p for p in parts if p]

    return get_env(name, cast=_cast, default=default, required=required)
