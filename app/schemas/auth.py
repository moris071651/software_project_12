from pydantic import BaseModel


class Register(BaseModel):
    name: str
    email: str
    password: str


class RegisterDoctor(Register):
    address: str


class RegisterPatient(Register):
    doctor_id: int
    phone: str


class Login(BaseModel):
    email: str
    password: str
    

class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True