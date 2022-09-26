from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import config.database as database
import routes.auth.hashing as hashing
from routes.auth import Token
from schemas import (ResLogin)


router = APIRouter(prefix="/Login", tags=['Login'])


def Create_token(data: dict):
    access_token = Token.create_access_token(
        data={"sub": data["email"], "isDoc": data["doctor"], "name": data["name"], "user_id": data["user_id"]})
    refresh_token = Token.create_refresh_token(
        data={"sub": data["email"], "isDoc": data["doctor"], "name": data["name"], "user_id": data["user_id"]})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


# for normal user
@router.post('/')
def login(info: OAuth2PasswordRequestForm = Depends()):

    cursor = database.user_col.find_one(
        {"email": info.username})  # finding in user collection
    if cursor:
        print("User Found")
        flag = hashing.verify_pass(info.password, cursor["password"])
        if flag == True:
            token = Create_token({
                "email": info.username,
                "doctor": False,
                "name": cursor["user"],
                "user_id": cursor["user_id"]
            })

            res = ResLogin(
                user_id=cursor["user_id"], access_token=token['access_token'], token_type=token['token_type'], user=cursor['user'], refresh_token=token['refresh_token'])

            return res
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    else:
        cursor = database.docs.find_one(
            {"email": info.username})  # finding in doc collection
        if cursor:
            print("Doc Found")
            flag = hashing.verify_pass(info.password, cursor["password"])
            if flag == True:
                token = Create_token({
                    "email": info.username,
                    "doctor": True,
                    "name": cursor["doc"],
                    "user_id": cursor["doc_id"]
                })

                res = ResLogin(
                    user_id=cursor["doc_id"],
                    access_token=token['access_token'],
                    token_type=token['token_type'],
                    user=cursor['doc'],
                    refresh_token=token['refresh_token'],
                    doctor=True
                )

                return res
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# get token payload


@router.get("/getPayLoad", status_code=200)
def getTokenDetails(token: str):
    try:
        return Token.getPayload(token)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
