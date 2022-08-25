import pytest
from rest_framework.reverse import reverse


@pytest.fixture
def headers():
    return {"content_type": 'application/json'}


@pytest.fixture
def register_user(client, django_user_model, headers):
    user_data = {"username": "Elavarasu", "password": "elavarasu123", "email": "elavarasu@gmail.com",
                 "first_name": "Elavarasu", "last_name": "Appusamy", "phone": 9807654321, "location": "Salem"}
    url = reverse('register')
    response = client.post(url, user_data, **headers)
    return response.data.get('data').get('id')