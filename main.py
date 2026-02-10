
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import User, Expense
from schemas import UserCreate, ExpenseOut, ExpenseCreate
from password_utlis import hash_password, verify_password
from jwt_utils import create_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from typing import List


# Use HTTPBearer instead of OAuth2PasswordBearer
bearer_scheme = HTTPBearer()

app = FastAPI()



# --- Database dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Home route ---
@app.get("/")
def greetings():
    return {"message": "Hello, Welcome to the Expense Tracker API!"}

# --- Signup route ---
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pwd = hash_password(user.password)
    db_user = User(username=user.username, hashed_password=hashed_pwd)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User created successfully"}

# --- Login route ---
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == form_data.username).first()

    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_token({"sub": db_user.username})

    return {"access_token": token, "token_type": "bearer"}

# --- Show all users (for testing) ---
@app.get("/show")
def show_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# --- Add expense (protected) ---
@app.post("/add_expenses", response_model=ExpenseOut)
def add_expense(
    expense: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):  
    print("token recieved",current_user.username)
    db_expense = Expense(
        user_id=current_user.id,
        amount=expense.amount,
        date=expense.date
    )
    
    existing = db.query(Expense).filter(Expense.user_id == current_user.id, Expense.date == expense.date).first()

    if existing:
        existing.amount += expense.amount
        db.commit()
        db.refresh(existing)
        return existing
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# --- Get my expenses (protected) ---
@app.get("/get_expenses", response_model=List[ExpenseOut])
def get_my_expenses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    return expenses
