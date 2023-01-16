from fastapi import FastAPI, status, Response, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
	title: str
	content: str
	published: bool = True

my_posts = [{"title": "Delicious Foods!", "content": "Eat aloo gobi :)", "id": 1},
			{"title": "Favorite Movie", "content": "2001: A Space Odyssey", "id": 2}]

def find_post(id):
	for index, post in enumerate(my_posts):
		if post["id"] == id:
			return (index, post)
	return 

@app.get("/")
def root():
    return {"message": "Welcome to my API!"}


@app.get("/posts")
def read_all_posts():
	return {"data": my_posts}


@app.get("/posts/{id}")
def read_single_post(id: int):
	post_detail = find_post(id)
	if not post_detail:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f"post with id: {id} does not exist.")
	post = post_detail[1]
	return {"post_detail": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
	post_dict = post.dict()
	post_dict["id"] = randrange(0, 100000000)
	my_posts.append(post_dict)
	return {"data": post_dict}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
	old_post_detail = find_post(id)
	if not old_post_detail:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f"post with id: {id} does not exist.")
	post_dict = post.dict()
	post_dict["id"] = id
	my_posts[old_post_detail[0]] = post_dict
	return {"data": post_dict}


@app.delete("/posts/{id}")
def delete_post(id: int):
	post_detail = find_post(id)
	if not post_detail:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f"post with id: {id} does not exist.")
	index = post_detail[0]
	my_posts.pop(index)
	return Response(status_code=status.HTTP_204_NO_CONTENT)