import pytest
from rest_framework.reverse import reverse


class TestUser:
    @pytest.mark.django_db
    def test_user_register_should_return_created_status(self, client, django_user_model, headers):
        user_data = {"username": "Elavarasu", "password": "elavarasu123", "email": "elavarasu@gmail.com",
                     "first_name": "Elavarasu", "last_name": "Appusamy", "phone": 9807654321, "location": "Salem"}
        url = reverse('register')
        response = client.post(url, user_data, **headers)
        assert response.status_code == 201
        assert response.data.get('data').get('username') == "Elavarasu"

    @pytest.mark.django_db
    def test_user_login_should_return_accepted_status(self, client, django_user_model, headers):
        user_data = {"username": "Elavarasu", "password": "elavarasu123", "email": "elavarasu@gmail.com",
                     "first_name": "Elavarasu", "last_name": "Appusamy", "phone": 9807654321, "location": "Salem"}
        url = reverse('register')
        post_response = client.post(url, user_data, **headers)
        assert post_response.status_code == 201
        url = reverse('login')
        login_data = {"username": "Elavarasu", "password": "elavarasu123"}
        response = client.post(url, login_data, **headers)
        assert response.status_code == 202

    @pytest.mark.django_db
    def test_invalid_user_login_should_return_bad_request_status(self, client, django_user_model, headers):
        user_data = {"username": "Elavarasu", "password": "elavarasu123", "email": "elavarasu@gmail.com",
                     "first_name": "Elavarasu", "last_name": "Appusamy", "phone": 9807654321, "location": "Salem"}
        url = reverse('register')
        post_response = client.post(url, user_data, **headers)
        assert post_response.status_code == 201
        url = reverse('login')
        login_data = {"username": "Elavarasu", "password": "123"}
        response = client.post(url, login_data, **headers)
        assert response.status_code == 400
        assert response.data.get('message') == "Invalid Credentials"
