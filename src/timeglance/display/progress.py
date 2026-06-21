from __future__ import annotations


def progress_bar(progress: float | None, width: int = 20) -> str:
    if progress is None:
        return "[" + "?" * width + "]"
    filled = max(0, min(width, round(progress * width)))
    return "[" + "#" * filled + "-" * (width - filled) + "]"
