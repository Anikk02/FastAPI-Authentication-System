import pytest
import uuid

@pytest.mark.asyncio
async def test_get_current_user_token(client):
    unique_email = f"aniket_{uuid.uuid4()}@example.com"

    register_payload = {
        "name": "Aniket",
        "email": unique_email,
        "password": "strongpass123"
    }

    # ✅ Register user
    res = await client.post("/auth/register", json=register_payload)
    assert res.status_code in (200, 201)

    # ✅ Login
    login_response = await client.post(
        "/auth/login",
        json={
            "email": unique_email,
            "password": "strongpass123"
        }
    )
    assert login_response.status_code == 200

    login_data = login_response.json()
    assert "access_token" in login_data

    token = login_data["access_token"]

    # ✅ Access protected route
    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["email"] == unique_email
    assert data["name"] == "Aniket"


@pytest.mark.asyncio
async def test_get_current_user_without_token(client):
    response = await client.get("/auth/me")

    # Depends on FastAPI security config
    assert response.status_code in (401, 403)