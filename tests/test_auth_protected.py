import pytest

@pytest.mark.asyncio
async def test_get_current_user_token(client):
    register_payload = {
        "name": "Aniket",
        "email": "aniket@example.com",
        "password": "strongpass123"
    }

    # ✅ Register user
    res = await client.post("/auth/register", json=register_payload)
    assert res.status_code == 201

    # ✅ Login
    login_response = await client.post(
        "/auth/login",
        json={
            "email": "aniket@example.com",
            "password": "strongpass123"
        }
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # ✅ Access protected route
    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "aniket@example.com"
    assert data["name"] == "Aniket"


@pytest.mark.asyncio
async def test_get_current_user_without_token(client):
    response = await client.get("/users/me")

    # FastAPI security may return 401 or 403 depending on config
    assert response.status_code in [401, 403]