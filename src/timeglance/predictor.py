from __future__ import annotations

from .models.forecast import Forecast
from .utils.confidence import confidence_from_durations


def risk_level(
    eta_seconds: float | None,
    estimated_peak_memory_mb: float | None,
    max_time_sec: float | None = None,
    max_ram_mb: float | None = None,
) -> str:
    score = 0
    if max_time_sec and eta_seconds is not None:
        if eta_seconds > max_time_sec:
            score += 2
        elif eta_seconds > max_time_sec * 0.8:
            score += 1
    if max_ram_mb and estimated_peak_memory_mb is not None:
        if estimated_peak_memory_mb > max_ram_mb:
            score += 2
        elif estimated_peak_memory_mb > max_ram_mb * 0.8:
            score += 1
    return ("LOW", "MEDIUM", "HIGH", "CRITICAL")[min(score, 3)]


def build_forecast(
    *,
    completed: int,
    total: int | None,
    elapsed_seconds: float,
    durations: list[float],
    current_memory_mb: float | None = None,
    peak_memory_mb: float | None = None,
    baseline_memory_mb: float | None = None,
    sample_size: int = 20,
    max_time_sec: float | None = None,
    max_ram_mb: float | None = None,
) -> Forecast:
    average = elapsed_seconds / completed if completed else 0.0
    throughput = completed / elapsed_seconds if elapsed_seconds > 0 else 0.0
    estimated_total = average * total if total is not None and completed else None
    eta = max(0.0, estimated_total - elapsed_seconds) if estimated_total is not None else None

    estimated_peak = peak_memory_mb
    if total and completed and current_memory_mb is not None and baseline_memory_mb is not None:
        growth = max(0.0, current_memory_mb - baseline_memory_mb)
        estimated_peak = baseline_memory_mb + (growth / completed * total)
        if peak_memory_mb is not None:
            estimated_peak = max(estimated_peak, peak_memory_mb)

    return Forecast(
        completed=completed,
        total=total,
        elapsed_seconds=elapsed_seconds,
        estimated_total_seconds=estimated_total,
        eta_seconds=eta,
        throughput_per_second=throughput,
        confidence=confidence_from_durations(durations, sample_size),
        current_memory_mb=current_memory_mb,
        peak_memory_mb=peak_memory_mb,
        estimated_peak_memory_mb=estimated_peak,
        risk_level=risk_level(eta, estimated_peak, max_time_sec, max_ram_mb),
    )
