from fastapi import FastAPI, status, Response, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# ROOT
@app.get("/")
def root():
    return {"message": "Welcome to my API!"}


# READ all posts
@app.get("/posts", response_model=list[schemas.PostResponse])
def read_all_posts(db: Session = Depends(get_db), ):
	posts = db.query(models.Post).all()
	return posts


# READ single post
@app.get("/posts/{id}", response_model=schemas.PostResponse)
def read_single_post(id: int, db: Session = Depends(get_db)):
	post = db.query(models.Post).filter(models.Post.id == id).first()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f"post with id: {id} does not exist.")
	return post


# CREATE post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostClient, db: Session = Depends(get_db)):
	created_post = models.Post(**post.dict())
	db.add(created_post)
	db.commit()
	db.refresh(created_post)
	return created_post


# UPDATE post
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostClient, db: Session = Depends(get_db)):
	post_query = db.query(models.Post).filter(models.Post.id == id)
	if not post_query.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f"post with id: {id} does not exist.")
	post_query.update(updated_post.dict(), synchronize_session=False)
	db.commit()
	return post_query.first()


# DELETE post
@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
	deleted_post = db.query(models.Post).filter(models.Post.id == id)
	if not deleted_post.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f"post with id: {id} does not exist.")
	deleted_post.delete(synchronize_session=False)
	db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)