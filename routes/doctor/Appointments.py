from fastapi import Depends, APIRouter, HTTPException, status
import uuid
from datetime import date
import config.database as database
from routes.auth import oauth2
import email_sender.appointment_notification as appointment_notification
from routes.users.models import (User)
from routes.doctor.models import (Inc_appointment, Show_all_appointments,
                     Show_appointment, appointment)


router = APIRouter(tags=["User Appointment Route"], prefix="/userroute")

# CREATING A new appointment


@ router.post('/create', status_code=201)
def create_appointment(Inc_appointment: Inc_appointment, current_user: User = Depends(oauth2.get_current_user)):

    try:

        cursor = database.user_col.find_one(
            {"user_id": Inc_appointment.user_id})

        cursor_doc = database.docs.find_one({"doc_id": Inc_appointment.doc_id})

        if cursor and cursor_doc:

            # providing unique id to every post to track
            new_appointment_id = str(uuid.uuid4())

            # using schema to convert the incoming data
            appointed = appointment(
                appointment_id=new_appointment_id,
                online=Inc_appointment.online,
                doc_id=Inc_appointment.doc_id,
                user_id=Inc_appointment.user_id,
                date=Inc_appointment.date,
                time=Inc_appointment.time,
            )

            # for doc
            prev_appoints_docs = cursor_doc['appointments_inreview']
            prev_appoints_docs.append(dict(appointed))

            # for user
            prev_appoints_user = cursor['appointments']
            prev_appoints_user.append(dict(appointed))

            myquery = {"user_id": Inc_appointment.user_id}
            newvalues = {"$set": {"appointments": prev_appoints_user}}
            updated = database.user_col.update_one(myquery, newvalues)

            myquery_doc = {"doc_id": Inc_appointment.doc_id}
            newvalues_doc = {
                "$set": {"appointments_inreview": prev_appoints_docs}}
            updated_doc = database.docs.update_one(myquery_doc, newvalues_doc)

            appointment_notification.appointment_email(
                Inc_appointment.doc_id, Inc_appointment.user_id, Inc_appointment.date, Inc_appointment.time, Inc_appointment.online)

            if not updated and not updated_doc:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# getting all the appointments by a particular user


@ router.post('/user/appoint', status_code=200)
def get_all_appointments(Show_all_appointments: Show_all_appointments, current_user: User = Depends(oauth2.get_current_user)):
    try:
        appointmentByUser = []
        appointmentByUserApproved = []
        cursor = database.user_col.find_one(
            {"user_id": Show_all_appointments.user_id})
        if cursor:
            for res in cursor['appointments']:
                appointmentByUser.append(appointment(**res))
            for res in cursor['approved_appointments']:
                appointmentByUserApproved.append(appointment(**res))

        return {"in_review": appointmentByUser, "approved": appointmentByUserApproved}

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@ router.post('/user_appointment_by_id', status_code=200)
def get_appointment(data: Show_appointment, current_user: User = Depends(oauth2.get_current_user)):

    try:
        cursor = database.user_col.find_one({"user_id": data.user_id})
        if cursor:
            for obj in cursor["appointments"]:
                if obj["appointment_id"] == data.appointment_id:
                    return appointment(**obj)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
