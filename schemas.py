from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    username: str
    password: str
    
class UserLogin(BaseModel):
    username: str
    password: str    
    
class ExpenseCreate(BaseModel):
    amount: float
    date: date
    
    
        