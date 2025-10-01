from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import  OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt

app = FastAPI()

#databse with username and password
user_db = {"user1": "pass1", "user2": "pass2"}

# Secret key to encode the JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Token class
class Token(BaseModel):
    access_token: str
    token_type: str
    
# Function to create JWT access token with expiration time
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES) #expiration time
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

def authenticate_user(username: str, password: str):
    if user_db.get(username) == password:
        return {"username": username}
    return HTTPException(status_code=401, detail="Invalid credentials")

#Login Endpoint
@app.post("/login", reponse_model = Token)
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form)
    access_token = create_access_token({"sub":user["username"]})
    token_type = "bearer"
    return {"access_token":access_token,"token_type": token_type}
    
    
    