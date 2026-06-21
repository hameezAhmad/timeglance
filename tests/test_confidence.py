from timeglance.utils.confidence import confidence_from_durations


def test_confidence_is_zero_without_samples():
    assert confidence_from_durations([]) == 0.0


def test_confidence_prefers_stable_samples():
    stable = confidence_from_durations([0.1, 0.1, 0.1, 0.1], sample_size=4)
    noisy = confidence_from_durations([0.01, 0.2, 0.03, 0.4], sample_size=4)

    assert stable > noisy
    assert stable <= 1.0
    assert noisy >= 0.0
