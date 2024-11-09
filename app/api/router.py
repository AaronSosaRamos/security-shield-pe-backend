#from app.api.features.schemas.schemas import RequestSchema, SpellingCheckerRequestArgs
from datetime import date
from http.client import HTTPException
import uuid
from fastapi import APIRouter, Depends, status, Request
import httpx
from app.api.logger import setup_logger
from app.api.auth.auth import (
    RegisterUser,
    Token,
    User,
    create_access_token, 
    key_check,
    return_db_instance
)
from passlib.hash import bcrypt

logger = setup_logger(__name__)
router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/user/register", response_model=Token)
async def register(user: RegisterUser):
    db = return_db_instance()
    if db["users"].find({"email": user.email}).count() > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado",
        )
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.ipify.org?format=json")
            response.raise_for_status()
            ip_signup = response.json().get("ip")
    except httpx.RequestError:
        ip_signup = "No disponible"
    
    hashed_password = bcrypt.hash(user.password)
    user_id = str(uuid.uuid4())
    db["users"].insert({
        "_key": user_id,
        "dni": user.dni,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "phone": user.phone,
        "email": user.email,
        "password": hashed_password,
        "department": user.department,
        "province": user.province,
        "district": user.district,
        "addressLine1": user.addressLine1,
        "birthDate": user.birthDate.isoformat(),
        "termsAccepted": user.termsAccepted,
        "ipSignup": ip_signup,
        "signupDate": date.today().isoformat()
    })
    access_token = create_access_token(data={"user_id": user_id, "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/user/login", response_model=Token)
async def login(user: User):
    db = return_db_instance()
    db_user = db["users"].find({"email": user.email}).next()
    if not db_user or not bcrypt.verify(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrecta",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"user_id": db_user["_key"], "email": db_user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/check-spelling")
# async def submit_tool( data: RequestSchema, _ = Depends(key_check)):
#     logger.info(f"Loading request args...")
#     args = SpellingCheckerRequestArgs(spelling_checker_schema=data)
#     logger.info(f"Args. loaded successfully")

#     chain = compile_chain()

#     logger.info("Generating the spelling checking analysis")
#     results = chain.invoke(args.validate_and_return())
#     logger.info("The spelling checking analysis has been successfully generated")

#     return results