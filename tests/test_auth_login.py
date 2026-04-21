import pytest

@pytest.mark.asyncio
async def test_login_success(client):
    register_payload = {
        "name": "Aniket",
        "email": "aniket@example.com",
        "password": "strongpass123"
    }

    # ✅ await added
    await client.post("/auth/register", json=register_payload)

    response = await client.post(
        "/auth/login",
        json={
            "email": "aniket@example.com",
            "password": "strongpass123"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    register_payload = {
        "name": "Aniket",
        "email": "aniket@example.com",
        "password": "strongpass123"
    }

    # ✅ await added
    await client.post("/auth/register", json=register_payload)

    response = await client.post(
        "/auth/login",
        json={
            "email": "aniket@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"