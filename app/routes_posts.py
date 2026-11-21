import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from app.database import get_session
from app.models import Post
router = APIRouter(prefix="/posts", tags=["posts"])
class PostCreate(BaseModel):
    title: str
    body_markdown: str
@router.post("", response_model=Post, status_code=201)
def create_post(data: PostCreate, session: Session = Depends(get_session)):
    if not data.title.strip() or not data.body_markdown.strip():
        raise HTTPException(status_code=422, detail="title and body_markdown must not be empty")
    post = Post(title=data.title.strip(), body_markdown=data.body_markdown.strip())
    session.add(post)
    session.commit()
    session.refresh(post)
    return post
@router.get("/{post_id}", response_model=Post)
def get_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post

class PostFromUrl(BaseModel):
    url: str
@router.post("/from-url", response_model=Post, status_code=201)
def create_post_from_url(data: PostFromUrl, session: Session = Depends(get_session)):
    try:
        resp = requests.get(data.url, timeout=10, headers={"User-Agent": "SocialStudioBot/1.0"})
        resp.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=422, detail=f"could not fetch url: {e}")
    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else data.url
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    body = "\n\n".join(p for p in paragraphs if p)
    if not body:
        raise HTTPException(status_code=422, detail="no readable text found at url")
    post = Post(title=title, source_url=data.url, body_markdown=body)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post
