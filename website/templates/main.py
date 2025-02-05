from fastapi import FastAPI, HTTPException, Request
from firebase_admin import credentials, initialize_app, auth, firestore
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi import Form
import os

# Initialize Firebase Admin SDK
cred = credentials.Certificate("M:/OKCU/Project/DocuMentor/website/templates/gaunlet.json")  # Correct path to your Firebase credentials file
initialize_app(cred)

# Initialize Firestore
db = firestore.client()

app = FastAPI()

# Route to serve the index.html page
@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    try:
        file_path = "M:/OKCU/Project/DocuMentor/website/templates/index.html"
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(content="Page not found", status_code=404)

# Route to serve the signup.html page
@app.get("/signup", response_class=HTMLResponse)
async def read_signup(request: Request):
    try:
        file_path = "M:/OKCU/Project/DocuMentor/website/templates/signup.html"
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(content="Page not found", status_code=404)

# Route to serve the login.html page
@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    try:
        file_path = "M:/OKCU/Project/DocuMentor/website/templates/login.html"
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(content="Page not found", status_code=404)

# Define data model for signup
class User(BaseModel):
    username: str
    email: str
    password: str

# Define data model for login
class UserLogin(BaseModel):
    email: str
    password: str

# Endpoint for user signup (POST method for form submission)
@app.post("/signup")
async def signup(user: User):
    try:
        # Check if the email already exists in Firebase Auth
        try:
            auth.get_user_by_email(user.email)
            raise HTTPException(status_code=400, detail="Email already in use")
        except auth.UserNotFoundError:
            pass  # If user not found, proceed to create the user

        # Create user in Firebase Authentication
        user_record = auth.create_user(
            email=user.email,
            password=user.password,
            display_name=user.username
        )

        # Store user in Firestore
        user_data = {
            "username": user.username,
            "email": user.email,
            "uid": user_record.uid
        }
        db.collection("users").document(user_record.uid).set(user_data)

        return {"message": "User created successfully", "uid": user_record.uid}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint for user login (POST method for form submission)
@app.post("/login")
async def login(user: UserLogin):
    try:
        # Sign in the user with Firebase Auth
        user_record = auth.get_user_by_email(user.email)
        
        # Verify password (Firebase Admin SDK does not directly verify passwords)
        # For the sake of simplicity, let's assume the credentials are correct.
        # You may need to use Firebase's client SDK in the frontend for real password verification.
        
        # In a production app, Firebase Admin SDK does not allow you to verify passwords.
        # You should use Firebase's client-side SDK to authenticate users.
        
        # Returning user UID and display name after successful login (in a real app, use JWT for session management)
        return {"message": "Login successful", "uid": user_record.uid, "username": user_record.display_name}
    
    except auth.AuthError:
        raise HTTPException(status_code=400, detail="Invalid credentials")

# Endpoint to get user details from Firestore
@app.get("/user/{uid}")
async def get_user(uid: str):
    try:
        # Fetch user data from Firestore using the UID
        user_ref = db.collection("users").document(uid)
        user_data = user_ref.get()

        if user_data.exists:
            return user_data.to_dict()
        else:
            raise HTTPException(status_code=404, detail="User not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
