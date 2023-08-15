from typing import Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/")
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = "")  -> list[schemas.PostOut]:
    
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
                 .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
                 .group_by(models.Post.id)
                 .filter(models.Post.title.icontains(search))
                 .limit(limit)
                 .offset(skip)
                 .all()
        )

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: schemas.UserOut = Depends(oauth2.get_current_user)) -> schemas.Post:
    
    new_post = models.Post(user_id=current_user.id, **post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)) -> schemas.PostOut:

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
                 .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
                 .group_by(models.Post.id)
                 .filter(models.Post.id == id)
                 .first()
        )
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)
    post_to_delete = post.first()

    if not (post_to_delete):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    if not post_to_delete.user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate,
                 db: Session = Depends(get_db), 
                 current_user: schemas.UserOut = Depends(oauth2.get_current_user)) -> schemas.Post:

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not (post):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    if not post.user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
