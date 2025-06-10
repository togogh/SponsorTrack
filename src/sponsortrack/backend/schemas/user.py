from pydantic import BaseModel, EmailStr, SecretStr, UUID4


class UserCreate(BaseModel):
    email: EmailStr
    password: SecretStr


class UserShow(BaseModel):
    id: UUID4
    email: EmailStr

    class Config:
        orm_mode = True
