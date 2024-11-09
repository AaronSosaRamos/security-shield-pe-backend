from datetime import date
from http.client import HTTPException
import uuid
from dotenv import find_dotenv, load_dotenv
from fastapi import APIRouter, Depends, status, Request
import httpx
from app.api.features.chatbot import chatbot_executor
from app.api.features.security_plan import compile_security_plan_chain
from app.api.logger import setup_logger
from app.api.auth.auth import (
    RegisterUser,
    Token,
    User,
    create_access_token,
    get_current_user, 
    key_check,
    return_db_instance
)
from passlib.hash import bcrypt
import os
from app.api.schemas.schemas import ChatRequest, ChatResponse, Message
from app.api.schemas.security_plan_schemas import SecurityPlanInput

logger = setup_logger(__name__)
router = APIRouter()

load_dotenv(find_dotenv())

@router.get("/")
def read_root():
    return {"Hello": "World"}

APIS_PE_TOKEN = os.getenv("APIS_PE_TOKEN")

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
            dni_response = await client.get(
                f"https://api.apis.net.pe/v2/reniec/dni?numero={user.dni}",
                headers={"Authorization": f"Bearer {APIS_PE_TOKEN}", "Accept": "application/json"}
            )
            dni_response.raise_for_status()
            dni_data = dni_response.json()
            numero_documento = dni_data.get("numeroDocumento")

            if numero_documento != user.dni:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El DNI proporcionado no es válido o no coincide con la información registrada en RENIEC."
                )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error al validar el DNI con el servicio de RENIEC."
        )

    try:
        async with httpx.AsyncClient() as client:
            ip_response = await client.get("https://api.ipify.org?format=json")
            ip_response.raise_for_status()
            ip_signup = ip_response.json().get("ip")
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

    access_token = create_access_token(data={
        "user_id": user_id,
        "email": user.email,
        "first_name": user.firstName,
        "last_name": user.lastName,
        "department": user.department,
        "province": user.province,
        "district": user.district
    })

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
    access_token = create_access_token(data={"user_id": db_user["_key"], 
                                             "email": db_user["email"], 
                                             "first_name": db_user["firstName"], 
                                             "last_name": db_user["lastName"],
                                             "department": db_user["department"],
                                             "province": db_user["province"],
                                             "district": db_user["district"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, token_data: dict = Depends(get_current_user)):
    user_name = request.user.fullName
    chat_messages = request.messages
    user_query = chat_messages[-1].payload.text

    response = chatbot_executor(user_name=user_name, user_query=user_query, messages=chat_messages)

    formatted_response = Message(
        role="ai",
        type="text",
        payload={"text": response}
    )

    return ChatResponse(data=[formatted_response])

@router.post("/security-plan")
async def security_plan( data: SecurityPlanInput, token_data: dict = Depends(get_current_user)):

    chain = compile_security_plan_chain()

    result = chain.invoke({
        "department": data.department,
        "province": data.province,
        "district": data.district,
        "mainTopic": data.mainTopic,
        "additionalDescription": data.additionalDescription
    })

    return result