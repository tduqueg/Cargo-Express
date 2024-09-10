import jwt
from datetime import datetime, timedelta

SECRET_KEY = "llave_super_secreta"

def crear_token(data:dict):
    payload = data.copy()
    payload.update({"exp": datetime.utcnow() + timedelta(minutes=30)})
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verificar_token(token:str):
    try:
        payload = jwt.decode (token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None