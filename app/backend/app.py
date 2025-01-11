from fastapi import FastAPI, HTTPException
from hashlib import sha256
from models import User
import os
import requests

# Load environment variables
from config import DATABASE, MODEL

# Create FastAPI instance
app = FastAPI()

@app.post('/register/')
async def register(user: User):
    
    # Hash password
    hashed_password = sha256(user.password.encode()).hexdigest()

    # Create data to send to database
    data = {
        "username": user.username,
        "email": user.email,
        "password_hash": hashed_password
    }

    # Check if user already exists
    try:
        response = requests.get(f'{DATABASE}/users/by-username/?username={user.username}')
        if response.status_code == 200:
            return {"detail": "User already exists"}
        response = requests.get(f'{DATABASE}/users/by-email/?email={user.email}')
        if response.status_code == 200:
            return {"detail": "Email already exists"}
    except:
        pass

    # Send data to database
    response = requests.post(f"{DATABASE}/users/", json=data)

    # Check if user was created
    if response.status_code == 201:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    