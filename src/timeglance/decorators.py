from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar

from .context import ForecastSession

F = TypeVar("F", bound=Callable[..., Any])


def forecast_function(func: F) -> F:
    """Decorate a function and attach the latest ForecastSession to the wrapper."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with ForecastSession() as session:
            result = func(*args, **kwargs)
        wrapper.latest_session = session  # type: ignore[attr-defined]
        return result

    wrapper.latest_session = None  # type: ignore[attr-defined]
    return wrapper  # type: ignore[return-value]
