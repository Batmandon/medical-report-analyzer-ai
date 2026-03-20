from pydantic import BaseModel, EmailStr, Field

class UserSignup(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserRefresh(BaseModel):
    token: str

class QuestionRequest(BaseModel):
    file_id: int
    question: str
