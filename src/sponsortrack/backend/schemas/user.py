from pydantic import BaseModel, EmailStr, SecretStr, Field, UUID4


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern="^[a-zA-Z0-9_.-]+$")
    email: EmailStr
    password: SecretStr


class UserShow(BaseModel):
    id: UUID4
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
