"""Functional tests for the Fruits API endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_list_fruits_empty(client: TestClient) -> None:
    resp = client.get("/fruits")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_fruit(client: TestClient) -> None:
    resp = client.post("/fruits", json={"fruit": "apple", "color": "red"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["fruit"] == "apple"
    assert body["color"] == "red"
    assert isinstance(body["id"], int)


def test_create_and_list_fruits(client: TestClient) -> None:
    client.post("/fruits", json={"fruit": "apple", "color": "red"})
    client.post("/fruits", json={"fruit": "banana", "color": "yellow"})

    resp = client.get("/fruits")
    assert resp.status_code == 200
    fruits = resp.json()
    assert len(fruits) == 2
    assert {f["fruit"] for f in fruits} == {"apple", "banana"}


def test_get_specific_fruit(client: TestClient) -> None:
    created = client.post("/fruits", json={"fruit": "grape", "color": "purple"}).json()
    fruit_id = created["id"]

    resp = client.get(f"/fruits/{fruit_id}")
    assert resp.status_code == 200
    assert resp.json() == {"id": fruit_id, "fruit": "grape", "color": "purple"}


def test_get_missing_fruit_returns_404(client: TestClient) -> None:
    resp = client.get("/fruits/9999")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()


def test_create_fruit_validation_error(client: TestClient) -> None:
    # Missing required "color" field.
    resp = client.post("/fruits", json={"fruit": "apple"})
    assert resp.status_code == 422


def test_create_fruit_rejects_empty_strings(client: TestClient) -> None:
    resp = client.post("/fruits", json={"fruit": "", "color": ""})
    assert resp.status_code == 422


def test_data_persists_across_requests(client: TestClient) -> None:
    """A created fruit is retrievable on a subsequent, independent request."""
    fruit_id = client.post("/fruits", json={"fruit": "kiwi", "color": "green"}).json()["id"]

    # Separate GET request hits the same backing store.
    resp = client.get(f"/fruits/{fruit_id}")
    assert resp.status_code == 200
    assert resp.json()["fruit"] == "kiwi"
