from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

# READ ALL posts
@router.get("/", response_model=list[schemas.PostResponse])
def read_all_posts(db: Session = Depends(get_db), 
					current_user: int = Depends(oauth2.get_current_user)):
	posts = db.query(models.Post).all()
	return posts


# READ post
@router.get("/{id}", response_model=schemas.PostResponse)
def read_post(id: int, db: Session = Depends(get_db), 
				current_user: int = Depends(oauth2.get_current_user)):
	post = db.query(models.Post).filter(models.Post.id == id).first()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f"post with id: {id} does not exist.")
	return post


# CREATE post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostClient, db: Session = Depends(get_db), 
				current_user: int = Depends(oauth2.get_current_user)):
	created_post = models.Post(**post.dict())
	db.add(created_post)
	db.commit()
	db.refresh(created_post)
	print(current_user.email)
	return created_post


# UPDATE post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostClient, db: Session = Depends(get_db), 
				current_user: int = Depends(oauth2.get_current_user)):
	post_query = db.query(models.Post).filter(models.Post.id == id)
	if not post_query.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f"post with id: {id} does not exist.")
	post_query.update(updated_post.dict(), synchronize_session=False)
	db.commit()
	return post_query.first()


# DELETE post
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), 
				current_user: int = Depends(oauth2.get_current_user)):
	deleted_post = db.query(models.Post).filter(models.Post.id == id)
	if not deleted_post.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f"post with id: {id} does not exist.")
	deleted_post.delete(synchronize_session=False)
	db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)