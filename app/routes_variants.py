from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from app.database import get_session
from app.generator import GENERATORS
from app.models import Post, Variant
from app.profiles import validate_variant
router = APIRouter(tags=["variants"])
class VariantCreate(BaseModel):
    post_id: int
    platform: str
    text: str
@router.post("/posts/{post_id}/variants", response_model=list[Variant], status_code=201)
def generate_variants(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    existing = {
        v.platform
        for v in session.exec(select(Variant).where(Variant.post_id == post_id)).all()
    }
    created = []
    for platform, make in GENERATORS.items():
        if platform in existing:
            continue
        text = make(post)
        errors = validate_variant(platform, text)
        if errors:
            raise HTTPException(status_code=422, detail=errors)
        variant = Variant(post_id=post_id, platform=platform, text=text)
        session.add(variant)
        created.append(variant)
    session.commit()
    for v in created:
        session.refresh(v)
    return created
@router.post("/variants", response_model=Variant, status_code=201)
def create_variant(data: VariantCreate, session: Session = Depends(get_session)):
    if not session.get(Post, data.post_id):
        raise HTTPException(status_code=404, detail="post not found")
    errors = validate_variant(data.platform, data.text)
    if errors:
        raise HTTPException(status_code=422, detail=errors)
    variant = Variant(post_id=data.post_id, platform=data.platform, text=data.text)
    session.add(variant)
    session.commit()
    session.refresh(variant)
    return variant
@router.get("/variants", response_model=list[Variant])
def list_variants(status: Optional[str] = None, session: Session = Depends(get_session)):
    query = select(Variant)
    if status:
        query = query.where(Variant.status == status)
    return session.exec(query).all()
