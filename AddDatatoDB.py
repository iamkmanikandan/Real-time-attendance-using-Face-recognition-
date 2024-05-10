import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("resource/DB/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendance-system-77a58-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

# first "" is key and inside{} is value
data = {
    "001":
        {
            "name": "Kesava Mahesh",
            "department": "CSE",
            "registration number": 950820104058,
            "semester": 6,
            "total_class": 0,
            "total_present": 0,
            "total_absent": 0,
            "year": 3,
            "last_attendance_time": '2023-05-16 14:18:50'
        },
    "002":
        {
            "name": "Zabiakliana",
            "department": "CSE",
            "registration number": 950820104054,
            "semester": 6,
            "total_present": 0,
            "total_absent": 0,
            "year": 3,
            "last_attendance_time": '2023-05-16 14:19:22'
        }
    # "003":
    #     {
    #         "name": "Manikandan",
    #         "department": "CSE",
    #         "registration number": 950820104054,
    #         "semester": 6,
    #         "total_class": 0,
    #         "total_present": 0,
    #         "total_absent": 0,
    #         "year": 3,
    #         "last_attendance_time": '2023-02-28 18:19:22'
    #     }
}

for key, value in data.items():
    ref.child(key).set(value)
