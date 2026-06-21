class TimeGlanceError(Exception):
    """Base exception for TimeGlance errors."""


class ForecastConfigurationError(TimeGlanceError, ValueError):
    """Raised when forecast options are invalid."""


class ExportError(TimeGlanceError):
    """Raised when a forecast report cannot be exported."""
