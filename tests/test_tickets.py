from app.models.event import Event


async def test_authenticated_user_can_purchase_ticket(client, db_session):
    user_payload = {
        "email": "customer@test.com",
        "password": "strongpassword123",
    }

    # Arrange: create a customer and obtain an access token.
    registration_response = await client.post(
        "/auth/register",
        json=user_payload,
    )
    assert registration_response.status_code == 200, registration_response.text
    user_id = registration_response.json()["id"]

    login_response = await client.post(
        "/auth/login",
        data={
            "username": user_payload["email"],
            "password": user_payload["password"],
        },
    )
    assert login_response.status_code == 200, login_response.text
    access_token = login_response.json()["access_token"]

    # Arrange: create an event with tickets available for purchase.
    event_response = await client.post(
        "/events/",
        json={
            "name": "Backend Bootcamp Live",
            "date": "2030-08-01T18:30:00+00:00",
            "total_tickets": 2,
            "available_tickets": 2,
        },
    )
    assert event_response.status_code == 200, event_response.text
    event_id = event_response.json()["id"]

    # Act
    ticket_response = await client.post(
        "/tickets/",
        json={"event_id": event_id},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Assert
    assert ticket_response.status_code == 200, ticket_response.text
    data = ticket_response.json()

    assert isinstance(data["id"], int)
    assert data["event_id"] == event_id
    assert data["user_id"] == user_id
    assert data["status"] == "reserved"
    assert isinstance(data["created_at"], str)

    event = await db_session.get(Event, event_id)
    assert event is not None

    await db_session.refresh(event)

    assert event.available_tickets == 1


async def test_ticket_purchase_requires_authentication(client):
    # Act: Send a request with a valid payload, but NO Authorization header
    response = await client.post("/tickets/", json={"event_id": 1})

    # Assert: The API should block it at the door
    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Not authenticated"


async def test_ticket_purchase_for_missing_event_returns_404(client):
    user_payload = {
        "email": "customer_404@test.com",
        "password": "strongpassword123",
    }

    # 1. Register and log in a user
    registration_response = await client.post(
        "/auth/register",
        json=user_payload,
    )
    assert registration_response.status_code == 200, registration_response.text

    login_response = await client.post(
        "/auth/login",
        data={
            "username": user_payload["email"],
            "password": user_payload["password"],
        },
    )
    assert login_response.status_code == 200, login_response.text
    access_token = login_response.json()["access_token"]

    # Request a ticket using a fake event ID with the bearer token.
    response = await client.post(
        "/tickets/",
        json={"event_id": 999999},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # 5. Assertions
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Event not found"


async def test_ticket_purchase_for_sold_out_event_returns_400(client):
    user_payload = {
        "email": "late_buyer@test.com",
        "password": "strongpassword123",
    }

    # 1. Register and log in a new user
    registration_response = await client.post(
        "/auth/register",
        json=user_payload,
    )
    assert registration_response.status_code == 200, registration_response.text

    login_response = await client.post(
        "/auth/login",
        data={
            "username": user_payload["email"],
            "password": user_payload["password"],
        },
    )
    assert login_response.status_code == 200, login_response.text
    access_token = login_response.json()["access_token"]

    # 2. Create an event with 0 available tickets
    event_response = await client.post(
        "/events/",
        json={
            "name": "Exclusive Sold-Out Concert",
            "date": "2030-08-15T20:00:00+00:00",
            "total_tickets": 1,
            "available_tickets": 0,
        },
    )
    assert event_response.status_code == 200, event_response.text
    event_id = event_response.json()["id"]

    # 3. Attempt to purchase from that event using the bearer token
    response = await client.post(
        "/tickets/",
        json={"event_id": event_id},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # 4. Assert
    assert response.status_code == 400, response.text
    assert response.json()["detail"] == "No tickets available"
