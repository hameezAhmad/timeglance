from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from .forecast import Forecast


@dataclass(frozen=True)
class Report:
    """Serializable report for a completed forecasted run."""

    forecast: Forecast
    created_at: str
    name: str = "timeglance"

    @classmethod
    def from_forecast(cls, forecast: Forecast, name: str = "timeglance") -> "Report":
        return cls(
            forecast=forecast,
            created_at=datetime.now(timezone.utc).isoformat(),
            name=name,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "created_at": self.created_at,
            "forecast": asdict(self.forecast),
        }
