from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta

app = FastAPI()

# Mock database with usernames and passwords
users_db = {"user1": "pass1", "user2": "pass2"}

# Configuration for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# TODO: Set up the OAuth2 scheme
# Define the OAuth2PasswordBearer instance with the token URL "login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/login")

# Token class
class Token(BaseModel):
    access_token: str
    token_type: str


# Function to create JWT token with an expiration time
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    

# Function to check if user exists in the database
def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if users_db.get(username) == password:
        return {"username": username}
    raise HTTPException(status_code=401, detail="Incorrect username or password")


# TODO: Get the current user from the JWT token
# Define a function `get_current_user` to decode and verify the JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid user")
    return {"user":username}
# Use `Depends` to extract the token using the OAuth2PasswordBearer instance
# Decode the token using `jwt.decode`
# Extract and return the username from the token payload
# Handle any JWT decoding errors by raising an HTTPException

# Login endpoint
@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Check username and password in database 
    user = authenticate_user(form_data)
    # Create an access token
    access_token = create_access_token(data={"sub": user["username"]})
    # Return the access token 
    return {"access_token": access_token, "token_type": "bearer"}


# TODO: Define a secured endpoint
@app.get("/secure-message")
async def secure_message(user: dict = Depends(get_current_user)):
    return {"message":"This is the secured message."}
# Create an endpoint `/secure-message` that is protected by the JWT token
# Use `Depends` with the `get_current_user` function to secure the endpoint
# Return a secured message