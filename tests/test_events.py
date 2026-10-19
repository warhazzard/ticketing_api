async def test_create_event(client):
    # Arrange
    event_payload = {
        "name": "Backend Engineering Conference",
        "date": "2030-06-15T18:30:00+00:00",
        "total_tickets": 100,
        "available_tickets": 100,
    }

    # Act
    response = await client.post("/events/", json=event_payload)
    # Assert
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == event_payload["name"]
    assert data["total_tickets"] == event_payload["total_tickets"]
    assert data["available_tickets"] == event_payload["available_tickets"]
    assert isinstance(data["id"], int)
    assert isinstance(data["date"], str)


async def test_create_event_rejects_non_positive_total_tickets(client):
    # Arrange
    event_payload = {
        "name": "Coding Bootcamp",
        "date": "2030-07-01T10:00:00+00:00",
        "total_tickets": 0,  # Invalid value
        "available_tickets": 0,
    }

    # Act
    response = await client.post("/events/", json=event_payload)

    # Assert
    assert response.status_code == 422, response.text
    errors = response.json()["detail"]

    assert any(error["loc"][-1] == "total_tickets" for error in errors)
