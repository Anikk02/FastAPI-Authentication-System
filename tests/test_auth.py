def test_register_user_success(client):
    response=client.post(
        '/auth/register',
        json = {
            'name':'Aniket',
            'email':'aniket@example.com',
            'password':'strongpass123'
        }
    )

    print(response.status_code)
    print(response.json())
    assert response.status_code ==201
    data = response.json()
    assert data['name']=='Aniket'
    assert data['email']=='aniket@example.com'
    assert 'id' in data
    assert 'hashed_password' not in data

def test_register_duplicate_email(client):
    payload = {
        'name':'Aniket',
        'email':'aniket@example.com',
        'password':'strongpass123'
    }

    client.post('/auth/register', json=payload)
    response = client.post('/auth/register', json=payload)

    assert response.status_code==400
    assert response.json()['detail']=='Email already registered'

def test_login_success(client):
    register_payload = {
        'name':'Aniket',
        'email':'aniket@example.com',
        'password':'strongpass123'
    }

    client.post('/auth/register',json=register_payload)

    response = client.post(
        '/auth/login',
        json = {
            'email':'aniket@example.com',
            'password':'strongpass123'
        }
    )

    assert response.status_code==200
    data = response.json()
    assert 'access_token' in data
    assert data['token_type']=='bearer'

def test_login_wrong_password(client):
    register_payload = {
        'name':'Aniket',
        'email':'aniket@example.com',
        'password':'strongpass123'
    }

    client.post('/auth/register',json = register_payload)

    response = client.post(
        '/auth/login',
        json = {
            'email':'aniket@example.com',
            'password':'wrongpassword'
        }
    )

    assert response.status_code ==401
    assert response.json()['detail']=='Invalid email or password'


def test_get_current_user_token(client):
    register_payload = {
        'name':'Aniket',
        'email':'aniket@example.com',
        'password':'strongpass123'
    }

    client.post('/auth/register',json=register_payload)

    login_response = client.post(
        '/auth/login',
        json={
            'email':'aniket@example.com',
            'password':'strongpass123'
        }
    )
    token = login_response.json()['access_token']

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    print(response.status_code)
    print(response.json())
    assert response.status_code==200
    data = response.json()
    assert data['email']=='aniket@example.com'
    assert data['name']=='Aniket'


def test_get_current_user_without_token(client):
    response = client.get('/users/me')
    assert response.status_code in [401,403]

