from email.utils import localtime
from fastapi import Depends, APIRouter, HTTPException, status
import config.database as database
import uuid
from routes.auth import oauth2
from schemas import (IntervalToken_inc, IntervalToken_ret, LocalitySearch,
                     Pre_doc, Signup_doc, User, del_appointment, doc_data, show_doc)
import email_sender.email_verification as email_verification
import routes.auth.hashing as hashing
from routes.auth import Token


router = APIRouter(tags=["Doc"], prefix="/doc")


@router.post('/create', status_code=201)
def create_doc(inc_doc: Signup_doc):

    try:
        etoken = Token.create_email_token(data={"sub": inc_doc.email})

        Docs = Pre_doc(
            doc=inc_doc.doc,
            password=hashing.hash_pass(inc_doc.password),
            email=inc_doc.email,
            doc_id=str(uuid.uuid4()),
            email_token=etoken,
            specialist_in=inc_doc.specialist_in,
            phone=inc_doc.phone,
            loc=inc_doc.loc,
            locality=inc_doc.locality,
            address=inc_doc.address,
            pincode=inc_doc.pincode
        )

        cursor2 = database.docs.find_one({"email": inc_doc.email})

        if cursor2:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        else:
            cursor1 = database.unverified_doc.find_one(
                {"email": inc_doc.email})
            if cursor1:
                cursor3 = database.unverified_doc.delete_one(
                    {"email": inc_doc.email})

            res = database.unverified_doc.insert_one(dict(Docs))
            email_verification.email(inc_doc.email, True)
            if not res:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/email_verification/{token}", status_code=200)
def verify_doc_email(token: str):
    # try:
    cursor = database.unverified_doc.find_one({"email_token": token})
    isValid = Token.verify_email_token(token)
    if not cursor or isValid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    doc = doc_data(
        doc=cursor['doc'],
        doc_id=cursor['doc_id'],
        email=cursor['email'],
        password=cursor['password'],
        specialist_in=cursor["specialist_in"],
        phone=cursor["phone"],
        loc=cursor["loc"],
        locality=cursor["locality"],
        address=cursor["address"],
        pincode=cursor["pincode"]
    )

    res = database.unverified_offline_doc.insert_one(dict(doc))

    if not res:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    dele = database.unverified_doc.delete_one({"email": cursor["email"]})
    if not dele:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    raise HTTPException(status_code=status.HTTP_201_CREATED)


@router.post("/doc_verification", status_code=200)
def verify_doc_token(rtoken: IntervalToken_inc):
    try:

        token = Token.verify_doc_token_at_call(rtoken.refresh_token)
        if token == None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return IntervalToken_ret(access_token=token)

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# verify doc post in person
@router.get("/doc_offline_verification/{doc_id}", status_code=200)
def verify_doc_offline(doc_id: str, current_user: User = Depends(oauth2.get_current_doc_user)):
    # try:
    cursor = database.unverified_offline_doc.find_one({"doc_id": doc_id})
    if not cursor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    doc = doc_data(
        doc=cursor['doc'],
        doc_id=cursor['doc_id'],
        email=cursor['email'],
        password=cursor['password'],
        specialist_in=cursor["specialist_in"],
        phone=cursor["phone"],
        loc=cursor["loc"],
        locality=cursor["locality"],
        address=cursor["address"],
        pincode=cursor["pincode"]
    )

    res = database.docs.insert_one(dict(doc))

    if not res:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    dele = database.unverified_offline_doc.delete_one(
        {"email": cursor["email"]})
    if not dele:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    raise HTTPException(status_code=status.HTTP_201_CREATED)


@router.get("/search/{locality}", status_code=200)
def getDocs(locality: str):
    try:
        doctors = []
        cursor = database.docs.find(
            {"locality": locality}).limit(15).sort("rating_avg", -1)
        if cursor:
            for res in cursor:
                doctors.append(LocalitySearch(
                    doc_id=res["doc_id"],
                    doc=res["doc"],
                    rating_avg=res["rating_avg"],
                    specialist_in=res["specialist_in"],
                    phone=res["phone"],
                    address=res["address"],
                    pincode=res["pincode"],
                )
                )

        return doctors
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@ router.get('/localdoc/{id}', status_code=200)
def getDoc(id):

    try:
        cursor = database.docs.find_one({"doc_id": id})
        if cursor:
            return show_doc(**cursor)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@ router.get('/approve', status_code=200)
def getDoc(approve: del_appointment, current_user: User = Depends(oauth2.get_current_doc_user)):

    try:
        cursor = database.docs.find_one({"doc_id": id})
        if cursor:
            # for doc
            new_to_review = []
            new_approved_to_doc = cursor['appointment_approved']
            newlyadded = {}

            for obj in cursor['appointment_inreview']:
                if not obj['appointment_id'] == approve.appointment_id:
                    new_to_review.append(obj)
                else:
                    new_approved_to_doc.append(obj)
                    newlyadded = obj

# for user
            cursor_user = database.user_col.find_one(
                {"user_id": newlyadded["user_id"]})

            prev_appoints_user = cursor_user['approved_appointments']
            prev_appoints_user.append(dict(newlyadded))

            new_to_review_user = []
            for obj in cursor_user['appointments']:
                if not obj['appointment_id'] == approve.appointment_id:
                    new_to_review_user.append(obj)

            myquery = {"user_id": newlyadded["user_id"]}
            newvalues = {"$set": {
                "approved_appointments": prev_appoints_user, "appointments": new_to_review_user}}
            updated = database.user_col.update_one(myquery, newvalues)

            myquery_doc = {"doc_id": approve.doc_id}
            newvalues_doc = {"$set": {
                "appointments_inreview": new_to_review, "appointments_approved": new_approved_to_doc}}

            updated_doc = database.docs.update_one(myquery_doc, newvalues_doc)

            # return show_doc(**cursor)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
