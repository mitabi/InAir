from pathlib import Path
import pytest
import pytest_socket
import os
from unittest.mock import patch
from custom_components.inair.api import (
    InPostAirApiClientConnectionError,
    InPostAirApiClientIdNotFoundError,
    InPostApi,
)
from custom_components.inair.models import (
    InPostAirPoint,
    InPostAirPointCoordinates,
)


@pytest.fixture()
def _allow_inpost_requests():
    pytest_socket.enable_socket()
    pytest_socket.socket_allow_hosts(["inpost.pl"])


@pytest.mark.parametrize("expected_lingering_timers", [True])
@pytest.mark.api
async def test_parcel_lockers_list(hass, _allow_inpost_requests):
    response = await InPostApi(hass).get_parcel_lockers_list()
    assert response is not None


@pytest.mark.parametrize("expected_lingering_timers", [True])
@pytest.mark.api
async def test_parcel_locker_search(hass, _allow_inpost_requests):
    response = await InPostApi(hass).search_parcel_locker("AJE01BAPP")
    assert response is not None


class FakeResponse:
    """Minimal aiohttp-like response for offline tests."""

    def __init__(self, text: str) -> None:
        self._text = text

    async def text(self) -> str:
        return self._text


PARCEL_LOCKER = InPostAirPoint(
    "AJE01BAPP",
    1,
    "Market Dino",
    "",
    "",
    "006",
    "Andrzejewo",
    "andrzejewo",
    "Warszawska",
    "mazowieckie",
    "07-305",
    "62A",
    "24/7",
    "[]",
    InPostAirPointCoordinates(52.83679, 22.20968),
    0,
    1,
)


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_find_parcel_locker_id_from_saved_html(hass):
    page = (
        Path(__file__).parent / "fixtures" / "parcel_locker_page_with_air.html"
    ).read_text(encoding="utf-8")
    response = FakeResponse(page)
    with patch.object(InPostApi, "_request", return_value=response):
        parcel_locker_id = await InPostApi(hass).find_parcel_locker_id(PARCEL_LOCKER)
    assert parcel_locker_id == "56311"


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_find_parcel_locker_id_html_without_marker_is_permanent(hass):
    page = (
        Path(__file__).parent / "fixtures" / "parcel_locker_page_without_air.html"
    ).read_text(encoding="utf-8")
    response = FakeResponse(page)
    with patch.object(InPostApi, "_request", return_value=response):
        with pytest.raises(InPostAirApiClientIdNotFoundError):
            await InPostApi(hass).find_parcel_locker_id(PARCEL_LOCKER)


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_find_parcel_locker_id_network_error_is_transient(hass):
    async def raise_connection_error(*args, **kwargs):
        raise InPostAirApiClientConnectionError("Cannot connect to API")

    with patch.object(InPostApi, "_request", side_effect=raise_connection_error):
        with pytest.raises(InPostAirApiClientConnectionError):
            await InPostApi(hass).find_parcel_locker_id(PARCEL_LOCKER)


@pytest.mark.skipif(
    os.environ.get("CI") == "true", reason="InPost blocks Github IP address"
)
@pytest.mark.parametrize("expected_lingering_timers", [True])
@pytest.mark.api
async def test_find_parcel_locker_id(hass, _allow_inpost_requests):
    response = await InPostApi(hass).find_parcel_locker_id(PARCEL_LOCKER)
    assert response is not None


@pytest.mark.skipif(
    os.environ.get("CI") == "true", reason="InPost blocks Github IP address"
)
@pytest.mark.parametrize("expected_lingering_timers", [True])
@pytest.mark.api
async def test_air_data(hass, _allow_inpost_requests):
    response = await InPostApi(hass).get_parcel_locker_air_data("AJE01BAPP", "56311")
    assert response is not None
