from pydantic import BaseModel, EmailStr, constr

class SignupRequest(BaseModel):
    username: constr(strip_whitespace=True, min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=6)

class LoginRequest(BaseModel):
    username: constr(strip_whitespace=True, min_length=3, max_length=50)
    password: constr(min_length=6)
