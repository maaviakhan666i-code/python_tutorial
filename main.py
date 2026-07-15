from fastapi import FastAPI, Form
from database import Base, engine, SessionLocal
from models import User
from passlib.hash import bcrypt

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/signup")
def signup(username: str = Form(...),
           email: str = Form(...),
           password: str = Form(...)):

    db = SessionLocal()

    user = User(
        username=username,
        email=email,
        password=bcrypt.hash(password)
    )

    db.add(user)
    db.commit()

    return {"message": "Signup Successful"}

@app.post("/login")
def login(email: str = Form(...),
          password: str = Form(...)):

    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    if user and bcrypt.verify(password, user.password):
        return {"message": "Login Successful"}

    return {"message": "Invalid Email or Password"}