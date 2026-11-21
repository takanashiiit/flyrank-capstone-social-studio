import re
from dataclasses import dataclass, field
@dataclass(frozen=True)
class Profile:
    platform: str
    max_length: int
    max_hashtags: int
    tone: str
    banned_phrases: tuple = field(default_factory=tuple)
PROFILES = {
    "telegram": Profile("telegram", 4096, 3, "conversational"),
    "x": Profile("x", 280, 2, "punchy, casual"),
    "linkedin": Profile(
        "linkedin", 3000, 5, "professional",
        banned_phrases=("lol", "omg", "wtf", "lmao"),
    ),
}
HASHTAG_PATTERN = re.compile(r"#\w+")
def validate_variant(platform: str, text: str) -> list[str]:
    """Return a list of broken rules. An empty list means the variant is valid."""
    profile = PROFILES.get(platform)
    if profile is None:
        return [f"unknown platform '{platform}'"]
    errors = []
    if not text.strip():
        errors.append("text must not be empty")
    if len(text) > profile.max_length:
        errors.append(
            f"max_length: {len(text)} chars exceeds the {profile.max_length} limit for {platform}"
        )
    hashtag_count = len(HASHTAG_PATTERN.findall(text))
    if hashtag_count > profile.max_hashtags:
        errors.append(
            f"max_hashtags: {hashtag_count} hashtags exceeds the {profile.max_hashtags} limit for {platform}"
        )
    lowered = text.lower()
    for phrase in profile.banned_phrases:
        if re.search(rf"\b{re.escape(phrase)}\b", lowered):
            errors.append(f"tone: '{phrase}' is not allowed for {platform} ({profile.tone})")
    return errors
