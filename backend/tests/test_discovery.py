from app.services.discovery import hysteresis_promote, hysteresis_demote


def test_promote():
    assert hysteresis_promote(3, 3) is True


def test_demote():
    assert hysteresis_demote(14, 14) is True
