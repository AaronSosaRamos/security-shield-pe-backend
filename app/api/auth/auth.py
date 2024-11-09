from datetime import date
from fastapi import (
  HTTPException, 
  Header, 
  FastAPI, 
  Depends, 
  status
)
import uuid
from pydantic import BaseModel
from typing import Optional
from jose import jwt
from arango import ArangoClient
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

def return_db_instance(): 
  client = ArangoClient()
  db = client.db(
        os.getenv("ARANGODB_DATABASE"),
        username=os.getenv("ARANGODB_USERNAME"),
        password=os.getenv("ARANGODB_PASSWORD"),
    )
  return db

class User(BaseModel):
    email: str
    password: str

class RegisterUser(BaseModel):
    dni: str
    firstName: str
    lastName: str
    phone: str
    email: str
    password: str
    confirmPassword: str
    department: str
    province: str
    district: str
    addressLine1: str
    birthDate: date
    termsAccepted: bool
    ipSignup: Optional[str] = None
    signupDate: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

#from google.cloud import secretmanager

# def access_secret_file(secret_id, version_id="latest"):
#     """
#     Access a secret file in Google Cloud Secret Manager and parse it.
#     """
#     project_id = os.environ.get('PROJECT_ID')
#     client = secretmanager.SecretManagerServiceClient()
#     name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
#     response = client.access_secret_version(name=name)
#     return response.payload.data.decode("UTF-8")

# Function to ensure incoming request is from controller with key
def key_check(api_key: str = Header(None)):
  
  if os.environ['ENV_TYPE'] == "production":
    #set_key = access_secret_file("backend-access")
    set_key = "production"
  else:
    set_key = "dev"
  
  if api_key is None or api_key != set_key:
    raise HTTPException(status_code=401, detail="Invalid API Request Key")