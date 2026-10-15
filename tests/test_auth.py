async def test_register_user(client):
    # Arrange 
    user_payload = {
        "email": "user005@example.com",
        "password": "pass12345"
    }
    
    # ACT
    response = await client.post("/auth/register", json=user_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user005@example.com"
    assert data["role"] == "customer"
    assert isinstance(data["id"], int)
    assert "hashed_password" not in data
    assert "password" not in data


async def test_register_duplicate_email(client):
    user_payload = {
        "email": "duplicate@example.com",
        "password": "secure-password"
    }

    first_response = await client.post("/auth/register", json=user_payload)
    second_response = await client.post("/auth/register", json=user_payload)

    assert first_response.status_code == 200, first_response.text
    assert second_response.status_code == 400, second_response.text
    assert second_response.json()["detail"] == "Email already registered"


async def test_user_login(client):
    # Arrange
    user_payload = {
        "email": "login@example.com",
        "password": "your-test-password",
    }

    registration_response = await client.post(
        "/auth/register",
        json=user_payload,
    )

    assert registration_response.status_code == 200, registration_response.text

    # Act
    login_response = await client.post(
        "/auth/login",
        data={
            "username": user_payload["email"],
            "password": user_payload["password"],
        },
    )

    # Assert
    assert login_response.status_code == 200, login_response.text

    data = login_response.json()
    assert isinstance(data["access_token"], str)
    assert data["access_token"]
    assert data["token_type"] == "bearer"


async def test_login_with_incorrect_password(client):
# Arrange
    user_payload = {
        "email": "wrongpass@example.com",
        "password": "correct-password",
    }

    # Register the user first so they exist in the system
    registration_response = await client.post(
        "/auth/register",
        json=user_payload,
    )
    assert registration_response.status_code == 200, registration_response.text

    # Act - Attempt login with a wrong password
    login_response = await client.post(
        "/auth/login",
        data={
            "username": user_payload["email"],
            "password": "completely-wrong-password",
        },
    )

    # Assert
    assert login_response.status_code in [400, 401], login_response.text
    data = login_response.json()
    assert "detail" in data 
