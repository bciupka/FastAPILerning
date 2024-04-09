from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict
from typing import Annotated


class ItemBase(BaseModel):
    title: Annotated[str, Field(max_length=100)]
    description: str | None = None


class ItemCreate(ItemBase): ...


class Item(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int


class UserBase(BaseModel):
    email: EmailStr
    about: str | None = None


class UserCreate(UserBase):
    password: str
    password2: str

    @model_validator(mode="after")
    def check_passwords(self) -> "UserCreate":
        if self.password == self.password2:
            return self
        raise ValueError("Passwords don't match")


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    items: list[Item] = []
