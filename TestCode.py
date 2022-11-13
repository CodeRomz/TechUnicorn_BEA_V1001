from TubeaDatabaseConnection import TubeaDbExec

view_appointment = TubeaDbExec("appointment")

for data in view_appointment.appointment_data_checker(1, 'doctor'):
    print(data)
