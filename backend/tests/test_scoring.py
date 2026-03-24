from app.services.scoring import compute_score


def test_score_computation_returns_tuple():
    score, rv, re = compute_score(
        views_velocity=120,
        engagement_velocity=20,
        acceleration=1.2,
        freshness_bonus=1,
        views_history=[10, 11, 12, 13],
        engagement_history=[2, 3, 2, 4],
        weights={"w1": 0.45, "w2": 0.3, "w3": 0.15, "w4": 0.1},
    )
    assert isinstance(score, float)
    assert rv > 0
    assert re > 0
