from TubeaDatabaseConnection import TubeaDbExec

view_appointment = TubeaDbExec("appointment")

datalist = []
for data in view_appointment.appointment_data_checker(1, 'doctor'):
    # print(data)
    datalist.append(data)


print(datalist)