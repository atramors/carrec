import requests

BASE = "http://127.0.0.1.5000"
data = [
    {
        "username": "Ron",
        "email": "ron@gmail.com",
        "password": 12345,
        "account_type": "User",
    },
    {
        "username": "John_car",
        "email": "dann@gmail.com",
        "password": 12345,
        "account_type": "Bussines",
    },
]
for i in data:
    first = requests.put(BASE + "user/" + str(i), data[i])
