from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    username: str
    password: str
    
class UserLogin(BaseModel):
    username: str
    password: str    
    
class ExpenseCreate(BaseModel):
    amount: int
    date: date
    
class ExpenseOut(BaseModel):
    id: int
    user_id: int
    amount: int
    date: date

    class Config:
        orm_mode = True
    
        