import pytest
import uuid

@pytest.mark.asyncio
async def test_login_success(client):
    unique_email = f"aniket_{uuid.uuid4()}@example.com"

    register_payload = {
        "name": "Aniket",
        "email": unique_email,
        "password": "strongpass123"
    }

    # Register user
    register_res = await client.post("/auth/register", json=register_payload)
    assert register_res.status_code in (200, 201)

    # Login
    response = await client.post(
        "/auth/login",
        json={
            "email": unique_email,
            "password": "strongpass123"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    unique_email = f"aniket_{uuid.uuid4()}@example.com"

    register_payload = {
        "name": "Aniket",
        "email": unique_email,
        "password": "strongpass123"
    }

    # Register user
    register_res = await client.post("/auth/register", json=register_payload)
    assert register_res.status_code in (200, 201)

    # Attempt login with wrong password
    response = await client.post(
        "/auth/login",
        json={
            "email": unique_email,
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"