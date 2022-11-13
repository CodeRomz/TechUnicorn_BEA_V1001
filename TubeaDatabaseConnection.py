from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://cluster0.wpk3oxf.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"

TubeaClient = MongoClient(uri, tls=True, tlsCertificateKeyFile='X509-cert-4444215937045702419.pem',
                          server_api=ServerApi('1'))
TubeaDb = TubeaClient['TechUnicorn_BEA']

class TubeaDbExec:

    def __init__(self, db_collection):
        self.db_collection = db_collection
        self.collection = TubeaDb[str(self.db_collection)]

    def add_user_data(self, user_id, fullname, email, password, access):
        self.collection.insert_one(
            {
            'user_id': user_id,
            'user_name': fullname,
            'user_password': password,
            'user_email': email,
            'user_access': access,
        }
        )

    def verify_login_data(self, user_email):
        self.user_email = user_email
        self.view_user_data = self.collection.find_one({"user_email": self.user_email})
        return self.view_user_data

    def book_appointment(self, doctor_id, patient_id, date, start_time, end_time, running_time, status):
        self.collection.insert_one(
            {
                "doctor_id": doctor_id,
                "patient_id": patient_id,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "running_time": running_time,
                "status": status
            }
        )

    def view_all_access(self, user_access):
        self.user_access = user_access
        db_all_data = list(self.collection.find({"user_access": self.user_access}, {'user_id': 1, 'user_name': 1, 'user_email': 1, '_id': 0}))
        return db_all_data

    def view_appointment_by_user_id(self, user_id, user_access):
        self.user_id = user_id
        self.user_access = user_access


        if user_access == 'doctor':
            db_all_data = list(self.collection.find({"doctor_id": int(self.user_id)}, {'patient_id': 1, 'doctor_id': 1, 'date': 1, '_id': 0, 'start_time': 1, 'end_time': 1, 'status': 1}))
            return db_all_data
        elif user_access == 'patient':
            db_all_data = list(self.collection.find({"patient_id": int(self.user_id)},
                                                    {'doctor_id': 1, 'date': 1, '_id': 0, 'start_time': 1,
                                                     'end_time': 1, 'status': 1}))
            return db_all_data

    def appointment_data_checker(self, user_id, user_access):
        self.user_id = user_id
        self.user_access = user_access

        if user_access == 'doctor':
            db_all_data = list(self.collection.find({"doctor_id": int(self.user_id)},
                                                    {'patient_id': 1, 'doctor_id': 1, 'date': 1, '_id': 0,
                                                     'start_time': 1, 'end_time': 1, 'status': 1, 'running_time':1}))
            return db_all_data
        elif user_access == 'patient':
            db_all_data = list(self.collection.find({"patient_id": int(self.user_id)},
                                                    {'doctor_id': 1, 'date': 1, '_id': 0, 'start_time': 1,
                                                     'end_time': 1, 'status': 1}))
            return db_all_data


# {'user_id': 1, 'doctor_id': 1, 'date': 1, '_id': 0, 'start_time': 1, 'end_time': 1, 'status': 1}