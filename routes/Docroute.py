from fastapi import Depends, APIRouter, HTTPException, status
import uuid
from datetime import date
import database
from routes import oauth2
import appointment_notification
from schemas import (Inc_appointment, Show_all_appointments, Show_appointment,User, appointment, del_appointment)

router = APIRouter(tags=["Doc Appointment Route"], prefix="/docroute")


# delete appointment and show for docs

@router.post('/delete', status_code=200)
def delete_appointment_only_docs(del_appointment: del_appointment, current_user: User = Depends(oauth2.get_current_doc_user)):
    try:
        cursor1 = database.user_col.find_one(
            {'doc_id': del_appointment.doc_id})
        if not cursor1:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

# doc
        new_appointments=[]
        new_deleted = {}
        for obj in cursor1['appointments_inreview']:
            if not obj["appointment_id"] == del_appointment.appointment_id:
                new_appointments.append(obj)
            else:
                new_deleted=obj
        
        myquery = {"doc_id": del_appointment.doc_id}
        newvalues = {"$set": {"appointments_inreview": new_appointments}}

# user

        cursor_user = database.user_col.find_one({"user_id":new_deleted["user_id"]})

        prev_appoints_user = cursor_user['appointments']
        new_appoints_user=[]
        for obj in prev_appoints_user:
            if not obj["appointment_id"] == del_appointment.appointment_id:
                new_appoints_user.append(obj)
            
        myquery = {"user_id": new_deleted["user_id"]}
        newvalues = {"$set": {"appointments": new_appoints_user}}
        updated = database.user_col.update_one(myquery, newvalues)

        database.user_col.update_one(myquery, newvalues)

    except:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



# get all the appointment from doctors point of view
@router.post("/appointments", status_code=200)
def get_all_doc_appointments(doc_id: str, current_user: User = Depends(oauth2.get_current_doc_user)):
    try:
        appointmentByUser = []
        cursor = database.docs.find(
            {"doc_id": id})
        if cursor:
            for res in cursor['appointments_inreview']:
                appointmentByUser.append(appointment(**res))
        appointmentByUser_approved = []
        for res in cursor['appointments_approved']:
            appointmentByUser.append(appointment(**res))

        return {"in_review":appointmentByUser,"approved":appointmentByUser_approved}

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
