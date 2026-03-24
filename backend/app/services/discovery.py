def hysteresis_promote(consecutive_hits: int, min_hits: int = 3) -> bool:
    return consecutive_hits >= min_hits


def hysteresis_demote(below_threshold_cycles: int, min_cycles: int = 14) -> bool:
    return below_threshold_cycles >= min_cycles
