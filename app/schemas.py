from pydantic import BaseModel
from datetime import datetime

class PostClient(BaseModel):
	title: str
	content: str
	published: bool = True

class PostResponse(BaseModel):
	id: int
	title: str
	content: str
	published: bool
	created_at: datetime

	class Config:
		orm_mode = True