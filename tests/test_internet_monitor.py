from unittest import mock

import requests

from internet_monitor import monitor


class DummyResponse:
    def __init__(self, status_code=200, chunks=None):
        self.status_code = status_code
        self._chunks = chunks or [b"x"]

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError("bad status")

    def iter_content(self, chunk_size=65536):
        for chunk in self._chunks:
            yield chunk

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_check_internet_up():
    with mock.patch.object(requests, "get", return_value=DummyResponse()) as get_mock:
        is_up, latency = monitor.check_internet(now=lambda: 1.0)
        assert is_up is True
        assert latency == 0.0
        get_mock.assert_called_once()


def test_check_internet_down():
    with mock.patch.object(requests, "get", side_effect=requests.RequestException("nope")):
        is_up, latency = monitor.check_internet(now=lambda: 5.0)
        assert is_up is False
        assert latency == 0.0


def test_run_speed_test_measurement():
    download_chunks = [b"x" * 2_000_000, b"x" * 3_000_000]
    response = DummyResponse(chunks=download_chunks)
    now_iter = iter([0.0, 1.0, 2.0, 3.0])
    now = lambda: next(now_iter)

    with mock.patch.object(requests, "get", return_value=response) as get_mock, mock.patch.object(
        requests, "post", return_value=DummyResponse()
    ) as post_mock:
        result = monitor.run_speed_test(
            download_bytes=5_000_000,
            upload_bytes=1_000_000,
            timeout=5.0,
            now=now,
        )

    assert result.download_bytes == 5_000_000
    assert result.upload_bytes == 1_000_000
    assert result.download_seconds == 1.0
    assert result.upload_seconds == 1.0
    assert result.download_mbps == 40.0
    assert result.upload_mbps == 8.0
    get_mock.assert_called_once()
    post_mock.assert_called_once()


def test_monitor_logs_speedtest_failure(tmp_path):
    log_path = tmp_path / "log.txt"
    logger = monitor.setup_logger(str(log_path))

    with mock.patch.object(monitor, "setup_logger", return_value=logger), mock.patch.object(
        monitor, "check_internet", return_value=(True, 0.1)
    ), mock.patch.object(
        monitor, "run_speed_test", side_effect=requests.RequestException("fail")
    ):
        monitor.monitor(
            log_path=str(log_path),
            check_interval=1,
            speedtest_interval=1,
            run_once=True,
        )

    contents = log_path.read_text()
    assert "Speed test failed" in contents
