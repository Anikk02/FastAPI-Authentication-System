def test_register_user_success(client):
    response = client.post(
        '/auth/register',
        json = {
            'name':'Aniket',
            'email':'aniket@example.com',
            'password':'strongpass123'
        }
    )

    assert response.status_code==201
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
    assert response.json()['detail']=="Email already registered"