from typing import Optional
from pydantic import BaseModel, EmailStr, Field

#review model
class review(BaseModel):
    doc_id:str=Field(...)
    author_id:str=Field(...)
    author:str=Field(...)
    body:str=Field(...)
    star_count:float = 0.0

# appointments

#appointments approved

class Inc_appointment(BaseModel):
    online:bool = True
    doc_id:str=Field(...)
    user_id:str=Field(...)
    date:str=Field(...)
    time:str=Field(...)

class appointment(BaseModel):
    appointment_id:str=Field(...)
    online:bool
    doc_id:str=Field(...)
    user_id:str=Field(...)
    date:str=Field(...)
    time:str=Field(...)
    approved:bool = False

# del appointment
class del_appointment(BaseModel):
    doc_id: str = Field(...)
    appointment_id: str = Field(...)

class Show_appointment(BaseModel):
    user_id:str=Field(...)
    appointment_id:str=Field(...)

class Show_all_appointments(BaseModel):
    user_id:str=Field(...)

# appointments


#signup doc
class Signup_doc(BaseModel):
    doc:str = Field(...)
    email:EmailStr = Field(...)
    password:str = Field(...)
    specialist_in:str = Field(...)
    phone:str = Field(...)
    loc:list[float] = Field(...)
    locality:str = Field(...)
    address:str = Field(...)
    pincode:str = Field(...)

#before validation doc
class Pre_doc(BaseModel):
    doc:str = Field(...)
    password:str = Field(...)
    email:EmailStr = Field(...)
    email_token : str=Field(...)
    specialist_in:str = Field(...)
    phone:str = Field(...)
    loc:list[float] = Field(...)
    locality:str = Field(...)
    address:str = Field(...)
    pincode:str = Field(...)
    doc_id:str = Field(...)

#final model for doc after validation
class doc_data(BaseModel):
    doc_id:str = Field(...)
    doc:str = Field(...)
    rating_avg:float = 0.0
    appointment_count:int = 0
    appointments_approved:list[dict] = []
    appointments_inreview:list[dict] = []
    reviews:list[dict] = []
    email:EmailStr = Field(...)
    password:str = Field(...)
    specialist_in:str = Field(...)
    phone:str = Field(...)
    loc:list[float] = Field(...)
    locality:str = Field(...)
    address:str = Field(...)
    pincode:str = Field(...)

# shows on clicking the local doctor
class show_doc(BaseModel):
    doc_id:str = Field(...)
    doc:str = Field(...)
    rating_avg:float = 0.0
    appointment_count:int = 0
    reviews:list[dict] = []
    email:EmailStr = Field(...)
    specialist_in:str = Field(...)
    phone:str = Field(...)
    loc:list[float] = Field(...)
    locality:str = Field(...)
    address:str = Field(...)
    pincode:str = Field(...)

class LocalitySearch(BaseModel):
    doc_id:str = Field(...)
    doc:str = Field(...)
    rating_avg:float = 0.0
    specialist_in:str = Field(...)
    phone:str = Field(...)
    address:str = Field(...)
    pincode:str = Field(...)
# doc model complete

#user model

#user signup
class User(BaseModel):
    user: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

# before validating user
class Pre_userdata(BaseModel):
    user: str = Field(...)
    password: str = Field(...)
    email: EmailStr = Field(...)
    user_id: str = Field(...)
    email_token: str = Field(...)

# after validation of user
class User_data(BaseModel):
    user: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    user_id: str = Field(...)
    appointments :list[dict] = []
    approved_appointments :list[dict] = []


#user model complete

#Login model
#from front end    
class Login(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

#from backend to frontend after login
class ResLogin(BaseModel):
    user: str = Field(...)
    user_id: str = Field(...)
    access_token: str = Field(...)
    refresh_token: str = Field(...)
    token_type: str = Field(...)
    doctor:bool = False

# verify on set interval
class IntervalToken_inc(BaseModel):
    refresh_token: str


class IntervalToken_ret(BaseModel):
    access_token: str

# used in verification of token data
class TokenData(BaseModel):
    email: Optional[str] = None

# class TokenDataPayload(BaseModel):
#     sub: Optional[str] = None
#     name:str
#     user_id:str
#     doctor:bool

#Login model

