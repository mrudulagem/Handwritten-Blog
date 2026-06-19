import pytest
from unittest.mock import patch, MagicMock
import os

os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault('SUPABASE_URL', 'https://test.supabase.co')
os.environ.setdefault('SUPABASE_SERVICE_ROLE_KEY', 'test-service-role-key')


@pytest.fixture
def client():
    with patch('supabase.create_client') as mock_create:
        mock_create.return_value = MagicMock()
        import app as flask_app
        flask_app.app.config['TESTING'] = True
        flask_app.app.config['WTF_CSRF_ENABLED'] = False
        with flask_app.app.test_client() as c:
            yield c, flask_app.supabase


def test_login_success_redirects_to_admin(client):
    c, mock_supabase = client
    mock_user = MagicMock()
    mock_user.user.id = 'user-123'
    mock_user.user.email = 'author@example.com'
    mock_supabase.auth.sign_in_with_password.return_value = mock_user

    response = c.post('/login', data={'email': 'author@example.com', 'password': 'correct'})

    assert response.status_code == 302
    assert '/admin' in response.headers['Location']


def test_login_failure_shows_error(client):
    c, mock_supabase = client
    mock_supabase.auth.sign_in_with_password.side_effect = Exception('Invalid credentials')

    response = c.post('/login', data={'email': 'wrong@example.com', 'password': 'wrong'})

    assert response.status_code == 200
    assert b'Invalid email or password' in response.data


def test_admin_route_blocked_when_logged_out(client):
    c, _ = client
    response = c.get('/admin')

    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_root_route_blocked_when_logged_out(client):
    c, _ = client
    response = c.get('/')

    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_upload_route_blocked_when_logged_out(client):
    c, _ = client
    response = c.post('/upload')

    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_admin_accessible_when_logged_in(client):
    c, mock_supabase = client
    mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = []

    with c.session_transaction() as sess:
        sess['user_id'] = 'user-123'
        sess['user_email'] = 'author@example.com'

    response = c.get('/admin')
    assert response.status_code == 200


def test_session_is_permanent_after_login(client):
    # Regression for AUTH-2: session.permanent = True must cause Flask to set
    # an Expires/Max-Age on the session cookie so it survives browser close.
    c, mock_supabase = client
    mock_user = MagicMock()
    mock_user.user.id = 'user-123'
    mock_user.user.email = 'author@example.com'
    mock_supabase.auth.sign_in_with_password.return_value = mock_user

    response = c.post('/login', data={'email': 'author@example.com', 'password': 'correct'})

    set_cookie = response.headers.get('Set-Cookie', '')
    assert 'Expires' in set_cookie or 'Max-Age' in set_cookie, (
        'Session cookie has no Expires/Max-Age — session.permanent = True is not taking effect'
    )


def test_logout_clears_session(client):
    c, _ = client
    with c.session_transaction() as sess:
        sess['user_id'] = 'user-123'

    c.get('/logout')

    with c.session_transaction() as sess:
        assert 'user_id' not in sess
