from datetime import datetime

import uvicorn
from fastapi import FastAPI, Body, Depends

from TubeaSchema import AppointmentSchema, UserSchema
from TubeaDatabaseConnection import TubeaDbExec

from auth_bearer import JWTBearer
from auth_handler import signJWT


app = FastAPI()

@app.post("/register", tags=["Register a user"])
def create_user(user: UserSchema = Body(...)):

    register_user = TubeaDbExec("user")
    register_user.add_user_data(user.user_id, user.fullname, user.email, user.password, user.access)

    return str('JWT:'), signJWT(user.email)


@app.post("/login", tags=["Login"])
def user_login(user: UserSchema = Body(...)):

    verify_user = TubeaDbExec("user")

    uv_value = verify_user.verify_login_data(user.email)

    print('Email:', user.email)
    print('Password:', user.password)

    try:
        if uv_value['user_email'] == None or uv_value["user_password"] == None:
            return {
                "error": "Wrong login details! none"
            }
        elif uv_value['user_email'] == user.email and uv_value["user_password"] == user.password:

            global g_user_access
            g_user_access = uv_value['user_access']
            print('Access:', g_user_access)

            global g_user_id
            g_user_id = uv_value['user_id']
            print('User ID:', g_user_id)

            return str('JWT:'), signJWT(user.email)
        else:
            return {
                "error": "Wrong login details!"
            }
    except Exception as e:
        print(e)
        return {
            "error": "Wrong login details! exept"
        }


@app.post("/book_appointment", dependencies=[Depends(JWTBearer())], tags=["Book an appointment"])
def add_post(appointment: AppointmentSchema):

    book_appointment = TubeaDbExec("appointment")

    timeFormat = '%H:%M:%S'

    s_time = datetime.strptime(appointment.start_time, timeFormat)
    e_time = datetime.strptime(appointment.end_time, timeFormat)

    running_time = e_time - s_time

    max_time = datetime.strptime('2:00:00', timeFormat)
    max_time_compare = datetime.strptime('00:00:00', timeFormat)

    min_time = datetime.strptime('00:15:00', timeFormat)
    min_time_compare = datetime.strptime('00:00:00', timeFormat)

    max_timeCompare = max_time - max_time_compare

    min_timeCompare = min_time - min_time_compare

    print(running_time)
    print(max_timeCompare)
    print(min_timeCompare)




    # Time checking (Minimum Duration is 15 min, Max duration 2hrs)
    if running_time <= max_timeCompare and running_time >= min_timeCompare:
        book_appointment.book_appointment(appointment.doctor_id, appointment.patient_id, appointment.date, appointment.start_time, appointment.end_time, str(running_time), appointment.status)

        return {
            "data": "appointment added.",
            "reminder": "Be at the doctor's clinic 5 minutes before the scheduled appointment time and print or wirte you appointment number.",
            "APPOINTMENT NO.": "A;SIODJF;AOISDJF"
        }

    else:
        return {
            "Time Error": "Kindly check the start time and End time Minimum Duration is 15 min, Max duration 2hrs",
            "Total Time": str(running_time)
        }

@app.get("/doctors", tags=["Doctors"], description='List of doctors')
def view_doctors():
    view_doctor = TubeaDbExec("user")

    for data in view_doctor.view_all_access("doctor"):
        print(data)

    return view_doctor.view_all_access("doctor")

@app.get("/my_appointment", dependencies=[Depends(JWTBearer())] , tags=["My Appointment"], description='List of doctors')
def view_appointment():
    view_appointment = TubeaDbExec("appointment")

    for data in view_appointment.view_appointment_by_user_id(g_user_id, g_user_access):
        print(data)

    return view_appointment.view_appointment_by_user_id(g_user_id, g_user_access)

uvicorn.run(app, host="127.0.0.1", port=8000)


