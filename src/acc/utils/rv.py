"""
Random Variables utilities
"""
from scipy.stats import maxwell, truncnorm


def produce_intervals(size: int = 3_600) -> list[int]:
    """
    Generate random intervals between disturbances.

    Args:
        size: number of intervals to generate

    Returns:
        A list of intervals in seconds of size `size` with no duplicates.
    """
    intervals = maxwell.rvs(loc=5, scale=750, size=size)
    return sorted(list(set(map(int, intervals))))


def produce_inclinations(mean_inclination_flat: float = 0.0,
                         mean_inclination_uphill: float = 5.0,
                         mean_inclination_downhill: float = -5.0,
                         std_deviation: float = 1.0,
                         lower_bound: float = -7.0,
                         upper_bound: float = 7.0,
                         size: int = 3_600,
                         ) -> list[float]:
    """
    Generate random road inclinations in a pattern of flat, uphill, flat, downhill.

    Args:
        mean_inclination_flat: Mean inclination for flat roads.
        mean_inclination_uphill: Mean inclination for uphill roads.
        mean_inclination_downhill: Mean inclination for downhill roads.
        std_deviation: Standard deviation for the inclinations.
        lower_bound: Minimum possible inclination.
        upper_bound: Maximum possible inclination.
        size: Number of inclinations to generate.

    Returns:
        Ordered road inclinations.
    """
    segment_lengths = [100, 150, 100, 150]
    segment_means = [mean_inclination_flat, mean_inclination_uphill, mean_inclination_flat, mean_inclination_downhill]

    inclinations: list[float] = []

    for _ in range(1 + size // sum(segment_lengths)):
        for length, mean in zip(segment_lengths, segment_means):
            a = (lower_bound - mean) / std_deviation
            b = (upper_bound - mean) / std_deviation
            segment_inclinations = truncnorm.rvs(a, b, loc=mean, scale=std_deviation, size=length)
            inclinations.extend(segment_inclinations)

    return inclinations[:size]
