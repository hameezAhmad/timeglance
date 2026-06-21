from __future__ import annotations

import os
import tracemalloc


def ensure_tracing() -> None:
    if not tracemalloc.is_tracing():
        tracemalloc.start()


def current_memory_mb() -> float:
    ensure_tracing()
    current, _ = tracemalloc.get_traced_memory()
    return current / (1024 * 1024)


def peak_memory_mb() -> float:
    ensure_tracing()
    _, peak = tracemalloc.get_traced_memory()
    return peak / (1024 * 1024)


def process_memory_mb() -> float | None:
    try:
        if os.name == "nt":
            import ctypes
            import ctypes.wintypes

            class ProcessMemoryCounters(ctypes.Structure):
                _fields_ = [
                    ("cb", ctypes.wintypes.DWORD),
                    ("PageFaultCount", ctypes.wintypes.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t),
                    ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t),
                    ("PeakPagefileUsage", ctypes.c_size_t),
                ]

            counters = ProcessMemoryCounters()
            counters.cb = ctypes.sizeof(counters)
            handle = ctypes.windll.kernel32.GetCurrentProcess()
            ctypes.windll.psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb)
            return counters.WorkingSetSize / (1024 * 1024)

        import resource

        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        divisor = 1024 if os.uname().sysname != "Darwin" else 1024 * 1024
        return usage / divisor
    except Exception:
        return None
