from fastapi import FastAPI, status, Response, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
	try:
		conn = psycopg2.connect(host='localhost', database='pythonapi', user='postgres', 
								password='password', cursor_factory=RealDictCursor)
		cursor = conn.cursor()
		print("Database connection successful!")
		break
	except Exception as error:
		print("Database connection failed.")
		print("Error: ", error)
		time.sleep(2)


class Post(BaseModel):
	title: str
	content: str
	published: bool = True


@app.get("/")
def root():
    return {"message": "Welcome to my API!"}


# READ all posts
@app.get("/posts")
def read_all_posts():
	cursor.execute("""SELECT * FROM posts""")
	posts = cursor.fetchall()
	return {"data": posts}


# READ single post
@app.get("/posts/{id}")
def read_single_post(id: int):
	cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
	post = cursor.fetchone()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f"post with id: {id} does not exist.")
	return {"post_detail": post}


# CREATE post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
	cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
						RETURNING *""", (post.title, post.content, post.published))
	created_post = cursor.fetchone()
	conn.commit()
	return {"data": created_post}


# UPDATE post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
	cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s
						RETURNING *""", (post.title, post.content, post.published, str(id)))
	updated_post = cursor.fetchone()
	conn.commit()
	if not updated_post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f"post with id: {id} does not exist.")
	return {"data": updated_post}


# DELETE post
@app.delete("/posts/{id}")
def delete_post(id: int):
	cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
	deleted_post = cursor.fetchone()
	conn.commit()
	if not deleted_post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f"post with id: {id} does not exist.")
	return Response(status_code=status.HTTP_204_NO_CONTENT)