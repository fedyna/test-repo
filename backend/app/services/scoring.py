from statistics import median


def robust_z(value: float, history: list[float]) -> float:
    if not history:
        return 0.0
    med = median(history)
    abs_devs = [abs(v - med) for v in history]
    mad = median(abs_devs) or 1.0
    return (value - med) / (1.4826 * mad)


def compute_score(views_velocity: float, engagement_velocity: float, acceleration: float, freshness_bonus: float,
                  views_history: list[float], engagement_history: list[float],
                  weights: dict[str, float]) -> tuple[float, float, float]:
    rel_views = robust_z(views_velocity, views_history)
    rel_eng = robust_z(engagement_velocity, engagement_history)
    acc = max(-2.0, min(5.0, acceleration))
    total = (
        weights.get("w1", 0.45) * rel_views
        + weights.get("w2", 0.30) * rel_eng
        + weights.get("w3", 0.15) * acc
        + weights.get("w4", 0.10) * freshness_bonus
    )
    return total, rel_views, rel_eng


def explanation_payload(delta_views: int, views_velocity: float, relative_views_z: float, acceleration: float, cluster: str) -> dict:
    return {
        "why": f"24h views growth: +{delta_views} ({views_velocity:.1f}/h); velocity {relative_views_z:+.2f}σ vs channel baseline; acceleration {acceleration:+.2f}",
        "cluster": cluster,
    }
