from dataclasses import dataclass


@dataclass
class LongFormRule:
    min_duration_seconds: int = 90


def is_short_video(title: str, tags: list[str] | None, duration_seconds: int, min_duration_seconds: int = 90) -> bool:
    tags = tags or []
    title_l = (title or "").lower()
    joined_tags = " ".join(tags).lower()
    if duration_seconds < min_duration_seconds:
        return True
    if "#shorts" in title_l or "shorts" in title_l:
        return True
    if "#shorts" in joined_tags or "shorts" in joined_tags:
        return True
    return False
