import requests

url = "http://localhost:4001/api/users"
data = {
    "username": "user1",
    "first_name": "Dave",
    "last_name": "Westerveld",
    "email_address": "fake@fake.com",
    "password": "password",
}
response = requests.post(url, json=data)
assert response.json() == {
    "username": "user1",
    "email_address": "fake@fake.com",
    "first_name": "Dave",
    "last_name": "Westerveld",
    "id": 1,
}

url = "http://localhost:4001/api/users/1"
response = requests.get(url)
assert response.status_code == 401

response = requests.get(url, auth=("user1", "password"))
assert response.json() == {
    "username": "user1",
    "email_address": "fake@fake.com",
    "first_name": "Dave",
    "last_name": "Westerveld",
    "id": 1,
}

url = "http://localhost:4001/token"
data = {"username": "user1", "password": "password"}
response = requests.post(url, data=data)
assert response.status_code == 200
token_dict = response.json()
assert token_dict.keys() == {"access_token", "token_type"}

url = "http://localhost:4001/api/clients"
response = requests.get(url)
assert response.json() == {"detail": "Not authenticated"}
header = {"Authorization": "Bearer " + token_dict["access_token"]}
response = requests.get(url, headers=header)
assert response.json() == {"message": "Clients"}
