import pytest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace

def test_unauthorized_access(client):
    response = client.delete("/master/111")

    assert response.status_code == 401


def test_create_appointment_and_double_booking(
    client,
    appointment,
    master_id,
    service_id,
):

    assert appointment["status"] == "pending_payment"

    payload = {
        "user_name": "Test_Client",
        "user_phone": "1231231231",
        "master_id": master_id,
        "service_id": service_id,
        "start_datetime": "2026-07-06T12:00"
    }

    with patch(
        "app.api.appointments.cancel_unpaid_task.apply_async"
    ):
        response = client.post(
            "/appointments/appointment",
            json=payload
        )

    assert response.status_code == 400
    assert "booked" in response.json()["detail"]


@patch("app.services.payments_service.stripe.checkout.Session.create")
def test_create_payment(mock_create, client, appointment):

    mock_create.return_value.url = "http://fake-stripe.url"

    response = client.post(
        f"/payments/create-checkout-session/{appointment['id']}"
    )

    assert response.status_code == 200
    assert response.json()["checkout_url"] == "http://fake-stripe.url"


@patch("app.services.payments_service.stripe.Webhook.construct_event")
def test_successful_webhook(mock_webhook, client, appointment):

    with patch("app.api.appointments.cancel_unpaid_task.delay"):
        
        fake_event = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "metadata": {
                        "appointment_id": str(appointment["id"])
                    },
                    "payment_intent": "pi_test"
                }
            }
        }

        mock_webhook.return_value = fake_event

        response = client.post(
            "/payments/webhook",
            json={},
            headers={
                "Stripe-Signature": "fake_sig"
            }
        )

        assert response.status_code == 200
        assert response.json()["status"] == "success"


def test_get_master_and_user_appointments(
    client,
    admin_headers,
    master_id,
):

    response = client.get(
        f"/master/masters/{master_id}/appointments",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "confirmed"

def test_cancel_appointment(client, appointment):

    with patch("app.api.appointments.cancel_unpaid_task.delay"):

        response = client.post(
            f"/booking/cancel/{appointment['cancel_token']}"
        )

        assert response.status_code == 200
        assert response.json()["status"] == "cancelled"

        response = client.post(
            f"/booking/cancel/{appointment['cancel_token']}"
        )

        assert response.status_code == 400