"""Test downloads without contacting live servers."""

from unittest.mock import Mock

import pytest
import requests

from tennis_career.download import _download_text


URL = "https://www.tennisabstract.com/example.js"


def test_download_text_returns_response_text(monkeypatch):
    response = Mock(text="var example = [];")
    get = Mock(return_value=response)
    monkeypatch.setattr("tennis_career.download.requests.get", get)
    assert _download_text(URL) == "var example = [];"
    get.assert_called_once_with(URL, timeout=30)
    response.raise_for_status.assert_called_once()


@pytest.mark.parametrize(
    "status, error_type, message",
    [
        (404, ValueError, "was not found"),
        (503, ConnectionError, "request failed"),
    ],
)
def test_download_text_handles_http_errors(monkeypatch, status, error_type, message):
    response = Mock(status_code=status)
    response.raise_for_status.side_effect = requests.HTTPError(response=response)
    monkeypatch.setattr(
        "tennis_career.download.requests.get", Mock(return_value=response)
    )
    with pytest.raises(error_type, match=message):
        _download_text(URL)


def test_download_text_handles_timeout(monkeypatch):
    get = Mock(side_effect=requests.Timeout("Timed out"))
    monkeypatch.setattr("tennis_career.download.requests.get", get)
    with pytest.raises(ConnectionError, match="Could not connect"):
        _download_text(URL)