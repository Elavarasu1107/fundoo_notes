import pytest
from rest_framework.reverse import reverse


@pytest.fixture
def register_user(client, django_user_model, headers):
    user_data = {"username": "Elavarasu", "password": "elavarasu123", "email": "elavarasu@gmail.com",
                 "first_name": "Elavarasu", "last_name": "Appusamy", "phone": 9807654321, "location": "Salem"}
    url = reverse('register')
    response = client.post(url, user_data, **headers)
    return response.data.get('data').get('id')


@pytest.fixture
def headers(django_user_model, db):
    user = django_user_model.objects.create_user(username="Elavarasu", password="password",
                                                 email="sellamuthuappusamy@gmail.com", first_name="Elavarasu",
                                                 last_name="Appusamy", phone=9807654321, location="Salem",
                                                 is_verified=1)
    return {"content_type": "application/json", "HTTP_TOKEN": user.token}
