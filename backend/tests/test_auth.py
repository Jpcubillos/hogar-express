import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(
        username='tester',
        email='tester@example.com',
        password='testpassword123',
        display_name='Test User'
    )
    return user

@pytest.mark.django_db
def test_csrf_endpoint(client):
    url = reverse('auth_csrf')
    response = client.get(url)
    assert response.status_code == 200
    assert 'csrfToken' in response.json()

@pytest.mark.django_db
def test_login_success(client, test_user):
    url = reverse('auth_login')
    data = {
        'username': 'tester',
        'password': 'testpassword123'
    }
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 200
    assert response.json()['username'] == 'tester'
    assert response.json()['display_name'] == 'Test User'

@pytest.mark.django_db
def test_login_failure(client, test_user):
    url = reverse('auth_login')
    data = {
        'username': 'tester',
        'password': 'wrongpassword'
    }
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 400
    assert 'validation_error' in response.json()['code']

@pytest.mark.django_db
def test_me_unauthenticated(client):
    url = reverse('auth_me')
    response = client.get(url)
    assert response.status_code == 403  # DRF Default for unauthenticated

@pytest.mark.django_db
def test_me_authenticated(client, test_user):
    client.login(username='tester', password='testpassword123')
    url = reverse('auth_me')
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()['username'] == 'tester'

@pytest.mark.django_db
def test_logout(client, test_user):
    client.login(username='tester', password='testpassword123')
    url = reverse('auth_logout')
    response = client.post(url)
    assert response.status_code == 200
    assert response.json() == {'message': 'Sesión cerrada correctamente'}
