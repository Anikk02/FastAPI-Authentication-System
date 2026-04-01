def test_get_current_user_token(client):
    register_payload = {
        "name": "Aniket",
        "email": "aniket@example.com",
        "password": "strongpass123"
    }

    client.post("/auth/register", json=register_payload)

    login_response = client.post(
        "/auth/login",
        json={
            "email": "aniket@example.com",
            "password": "strongpass123"
        }
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "aniket@example.com"
    assert data["name"] == "Aniket"


def test_get_current_user_without_token(client):
    response = client.get("/users/me")
    assert response.status_code in [401, 403]