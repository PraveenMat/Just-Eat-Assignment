import pytest
import requests
from main import format_restaurant, get_restaurants

class DummyResponse:
    """
    Minimal fake response for testing get_restaurants.
    """
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise requests.HTTPError(f"HTTP {self.status_code}")


def test_format_restaurant_complete():
    restaurant = {
        "name": "Test Resto",
        "cuisines": [{"name": "Italian"}, {"name": "Pizza"}],
        "rating": {"starRating": 4.5},
        "address": {
            "firstLine": "1 Test St",
            "city": "Testville",
            "postalCode": "TE1 1ST",
        },
    }
    assert format_restaurant(1, restaurant) == [
        1,
        "Test Resto",
        "Italian, Pizza",
        4.5,
        "1 Test St, Testville, TE1 1ST",
    ]


def test_format_restaurant_missing_fields():
    # All fields should fall back to "N/A"
    assert format_restaurant(2, {}) == [2, "N/A", "N/A", "N/A", "N/A"]


def test_get_restaurants_success(monkeypatch):
    dummy = {"restaurants": [{"name": "X"}, {"name": "Y"}]}
    monkeypatch.setattr(
        requests, "get",
        lambda url, headers: DummyResponse(dummy)
    )
    result = get_restaurants("AB1 2CD", limit=1)
    assert result == [{"name": "X"}]


def test_get_restaurants_http_error(monkeypatch):
    # Simulate a non-2xx status code
    monkeypatch.setattr(
        requests, "get",
        lambda url, headers: DummyResponse({}, status_code=404)
    )
    with pytest.raises(requests.HTTPError):
        get_restaurants("ZZ9 9ZZ")
