import pytest
from rest_framework.reverse import reverse


class TestNotes:

    @pytest.mark.django_db
    def test_create_notes_should_return_created_status(self, client, register_user, headers):
        user_id = register_user
        note_data = {"title": "Python", "description": "Interpreted Language", "color": "Green", "user": user_id}
        url = reverse('note')
        response = client.post(url, note_data, **headers)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_get_notes_should_return_ok_status(self, client, register_user, headers):
        user_id = register_user
        note_data = {"title": "Python", "description": "Interpreted Language", "color": "Green", "user": user_id}
        url = reverse('note')
        post_response = client.post(url, note_data, **headers)
        assert post_response.status_code == 201
        get_response = client.get(url, {"user": user_id}, **headers)
        assert get_response.status_code == 200

    @pytest.mark.django_db
    def test_update_note_should_return_created_status(self, client, register_user, headers):
        user_id = register_user
        note_data = {"title": "Python", "description": "Interpreted Language", "color": "Green", "user": user_id}
        url = reverse('note')
        post_response = client.post(url, note_data, **headers)
        assert post_response.status_code == 201
        assert post_response.data.get('data').get('color') == "Green"
        note_id = post_response.data.get('data').get('id')
        new_data = {"id": note_id, "title": "Python", "description": "Interpreted Language", "color": "Yellow",
                    "user": user_id}
        put_response = client.put(url, new_data, **headers)
        assert put_response.status_code == 201
        assert put_response.data.get('data').get('color') == "Yellow"

    @pytest.mark.django_db
    def test_delete_note_should_return_no_content_status(self, client, register_user, headers):
        user_id = register_user
        note_data = {"title": "Python", "description": "Interpreted Language", "color": "Green", "user": user_id}
        url = reverse('note')
        post_response = client.post(url, note_data, **headers)
        note_id = post_response.data.get('data').get('id')
        delete_response = client.delete(url, {"id": note_id}, **headers)
        assert delete_response.status_code == 204
