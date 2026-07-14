import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_health_check(client):
    url = reverse('health_check')
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {'status': 'ok', 'message': 'Hogar Express backend is running'}

@pytest.mark.django_db
def test_ready_check(client):
    url = reverse('ready_check')
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()['status'] == 'ready'
