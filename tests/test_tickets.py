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
