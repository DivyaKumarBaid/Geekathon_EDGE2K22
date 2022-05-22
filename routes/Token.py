from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas
import database
import os
from fastapi import Depends, HTTPException, status


ACCESS_TOKEN_SECRET_KEY = "h7qdsGDSr6AGg9616-VPSEP0w18vgXnMpey3JHvNPq8"
REFRESH_TOKEN_SECRET_KEY = "IBLGcEAxWWKQ-_Gr4rNfaH0HhvnBbZuEm_xi3clioOs"
EMAIL_TOKEN_SECRET_KEY = "JF_GcOWLg-Ycz_h8Bv_7PvnSCV-n_OuLsWg2HXBCtU0"
ALGORITHM = "HS256"

# access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# refresh token
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=20)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# email token
def create_email_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=2)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, EMAIL_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#verify token at email
def verify_email_token(token: str):
    try:
        payload = jwt.decode(
            token, EMAIL_TOKEN_SECRET_KEY, algorithms=ALGORITHM)

        email: str = payload.get("sub")

        cursor = database.user_col.find_one({"email": email})

        if not cursor:
            return False

        return True

    except JWTError:
        return False


# admin token

# decode accesstoken
def verify_admin_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, ACCESS_TOKEN_SECRET_KEY, algorithms=ALGORITHM)

        email: str = payload.get("sub")
        print(email)
        cursor = database.admin.find_one({"email": email})

        if email is None or not cursor:
            raise credentials_exception

        return schemas.TokenData(email=email)

    except jwt.ExpiredSignatureError:
        return True

    except JWTError:
        raise credentials_exception

# admin token

# decode user accesstoken
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, ACCESS_TOKEN_SECRET_KEY, algorithms=ALGORITHM)

        email: str = payload.get("sub")
        print(email)
        cursor = database.user_col.find_one({"email": email})

        if email is None or not cursor:
            raise credentials_exception

        return schemas.TokenData(email=email)

    except jwt.ExpiredSignatureError:
        return True

    except JWTError:
        raise credentials_exception

#decode user refresh token
def verify_token_at_call(token: str):
    try:
        payload = jwt.decode(
            token, REFRESH_TOKEN_SECRET_KEY, algorithms=ALGORITHM)

        email: str = payload.get("sub")

        cursor = database.user_col.find_one({"email": email})

        if not cursor:
            return None

        return create_access_token(data={"sub": email})

    except JWTError:
        return None

# admin
# admin

# decode doc accesstoken
def verify_doc_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, ACCESS_TOKEN_SECRET_KEY, algorithms=ALGORITHM)

        email: str = payload.get("sub")
        print(email)
        cursor = database.docs.find_one({"email": email})

        if email is None or not cursor:
            raise credentials_exception

        return schemas.TokenData(email=email)

    except jwt.ExpiredSignatureError:
        return True

    except JWTError:
        raise credentials_exception

#decode user refresh token
def verify_doc_token_at_call(token: str):
    try:
        payload = jwt.decode(
            token, REFRESH_TOKEN_SECRET_KEY, algorithms=ALGORITHM)

        email: str = payload.get("sub")

        cursor = database.docs.find_one({"email": email})

        if not cursor:
            return None

        return create_access_token(data={"sub": email})

    except JWTError:
        return None


# admin
# admin

#decode to get payload
def getPayload(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, ACCESS_TOKEN_SECRET_KEY, algorithms=ALGORITHM)

        email: str = payload.get("sub")

        cursor = database.user_col.find_one({"email": email})

        if email is None or not cursor:
            raise credentials_exception

        return payload

    except jwt.ExpiredSignatureError:
        return True

    except JWTError:
        raise credentials_exception

