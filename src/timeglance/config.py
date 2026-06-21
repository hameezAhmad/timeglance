from __future__ import annotations

from dataclasses import dataclass

from .exceptions import ForecastConfigurationError


@dataclass(frozen=True)
class ForecastConfig:
    sample_size: int = 20
    update_every: int = 100
    max_ram_mb: float | None = None
    max_time_sec: float | None = None
    export: str | None = None

    def validate(self) -> "ForecastConfig":
        if self.sample_size < 1:
            raise ForecastConfigurationError("sample_size must be at least 1")
        if self.update_every < 1:
            raise ForecastConfigurationError("update_every must be at least 1")
        if self.max_ram_mb is not None and self.max_ram_mb <= 0:
            raise ForecastConfigurationError("max_ram_mb must be positive")
        if self.max_time_sec is not None and self.max_time_sec <= 0:
            raise ForecastConfigurationError("max_time_sec must be positive")
        return self
