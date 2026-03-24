from app.services.filters import is_short_video


def test_short_detection_duration():
    assert is_short_video("Long video", [], 60) is True


def test_short_detection_tag():
    assert is_short_video("Great #shorts", [], 500) is True


def test_long_form():
    assert is_short_video("Automation pipeline", ["n8n"], 600) is False
