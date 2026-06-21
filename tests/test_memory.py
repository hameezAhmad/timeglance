from timeglance.utils.memory import current_memory_mb, peak_memory_mb, process_memory_mb


def test_memory_helpers_return_non_negative_values():
    assert current_memory_mb() >= 0
    assert peak_memory_mb() >= 0

    process_memory = process_memory_mb()
    assert process_memory is None or process_memory >= 0
