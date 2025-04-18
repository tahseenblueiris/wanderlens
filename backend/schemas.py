from pydantic import BaseModel

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    country: str
    city: str
    state: str
    zipcode: str
    address: str
    mobile: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    country: str
    city: str
    state: str
    zipcode: str
    address: str
    mobile: str

    class Config:
        orm_mode = True
