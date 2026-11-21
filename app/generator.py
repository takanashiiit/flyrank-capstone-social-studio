import re
from app.models import Post
from app.profiles import PROFILES
def truncate(text: str, limit: int) -> str:
    """Cut text to at most `limit` characters, ending on a whole word."""
    if len(text) <= limit:
        return text
    cut = text[: limit - 3].rsplit(" ", 1)[0]
    return cut + "..."
def make_hashtags(title: str, count: int) -> str:
    """Build hashtags from the longer words in the title."""
    words = re.findall(r"[A-Za-z]{5,}", title)
    seen = []
    for w in words:
        tag = "#" + w.lower()
        if tag not in seen:
            seen.append(tag)
    return " ".join(seen[:count])
def first_sentence(body: str) -> str:
    return re.split(r"(?<=[.!?])\s+", body.strip())[0]
def paragraphs(body: str, n: int) -> str:
    parts = [p.strip() for p in body.split("\n\n") if p.strip()]
    return "\n\n".join(parts[:n])
def generate_x(post: Post) -> str:
    tags = make_hashtags(post.title, PROFILES["x"].max_hashtags)
    room = PROFILES["x"].max_length - len(tags) - 1
    return truncate(first_sentence(post.body_markdown), room) + " " + tags
def generate_telegram(post: Post) -> str:
    tags = make_hashtags(post.title, PROFILES["telegram"].max_hashtags)
    body = truncate(paragraphs(post.body_markdown, 2), 1500)
    return f"{post.title}\n\n{body}\n\n{tags}"
def generate_linkedin(post: Post) -> str:
    tags = make_hashtags(post.title, PROFILES["linkedin"].max_hashtags)
    body = truncate(paragraphs(post.body_markdown, 3), 1500)
    return f"{post.title}\n\n{body}\n\nWhat is your experience with this?\n\n{tags}"
GENERATORS = {
    "x": generate_x,
    "telegram": generate_telegram,
    "linkedin": generate_linkedin,
}
