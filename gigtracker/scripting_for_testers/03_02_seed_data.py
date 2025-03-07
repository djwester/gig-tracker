import faker
import requests

fake = faker.Faker()

base_url = "http://localhost:4001"


def create_venues(count: int = 5) -> list[int]:
    venue_ids = []
    for _ in range(count):
        response = requests.post(
            f"{base_url}/api/venues",
            json={
                "name": fake.text(max_nb_chars=20),
                "address": fake.address(),
                "contact_number": fake.phone_number(),
                "contact_email": fake.email(),
                "capacity": fake.random_number(digits=3),
                "notes": fake.paragraph(),
            },
        )
        venue_ids.append(response.json()["id"])

    # Create a duplicate venue
    response = requests.get(f"{base_url}/api/venues/{venue_ids[0]}")
    response = requests.post(f"{base_url}/api/venues", json=response.json())
    venue_ids.append(response.json()["id"])
    return venue_ids


def create_user():
    url = "http://localhost:4001/api/users"
    data = {
        "username": "user1",
        "first_name": "Dave",
        "last_name": "Westerveld",
        "email_address": "fake@fake.com",
        "password": "password",
    }

    response = requests.post(url, json=data)
    print(response.json())


def get_auth_token(username: str = "user1", password: str = "password") -> str:
    response = requests.get(f"{base_url}/token", auth=(username, password))
    if not response.status_code == 200:
        create_user()

    url = "http://localhost:4001/token"
    data = {"username": username, "password": password}
    response = requests.post(url, data=data)
    print(response.json())
    token_dict = response.json()

    return token_dict["access_token"]


def create_clients(count: int = 5) -> list[int]:
    auth_token = get_auth_token()
    header = {"Authorization": f"Bearer {auth_token}"}
    client_ids = []
    for _ in range(count):
        response = requests.post(
            f"{base_url}/api/clients",
            headers=header,
            json={
                "email_address": fake.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "phone_number": fake.phone_number(),
                "address": fake.address(),
                "city": fake.city(),
                "province": fake.state(),
                "zip": fake.postalcode(),
                "country": fake.country(),
            },
        )
        print(f"Created client: {response.json()}")
        print(f"Status: {response.status_code}")
        client_ids.append(response.json()["id"])
    return client_ids


def create_gigs(venue_ids: list[int], client_ids: list[int], count: int = 5):
    for _ in range(count):
        response = requests.post(
            f"{base_url}/api/gigs",
            json={
                "venue_id": fake.random_element(venue_ids),
                "client_id": fake.random_element(client_ids),
                "date": fake.date(),
                "time": fake.time(pattern="%H:%M"),
                "name": fake.text(max_nb_chars=20),
            },
        )
        print(f"Created gig: {response.json()}")


venue_ids = create_venues()
client_ids = create_clients()
create_gigs(venue_ids, client_ids)

# for _ in range(5):
#     response = requests.post(
#         f"{base_url}/api/gigs",
#         json={
#             "venue": fake.text(max_nb_chars=20),
#             "date": fake.date(),
#             "time": fake.time(pattern="%H:%M"),
#         },
#     )
#     print(f"Created gig: {response.json()}")
