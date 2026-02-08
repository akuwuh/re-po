"""Monitor internet connectivity and run periodic speed tests."""

from __future__ import annotations

import argparse
import logging
import time
from dataclasses import dataclass
from typing import Callable

import requests

CONNECTIVITY_URL = "https://www.google.com/generate_204"
DOWNLOAD_TEST_URL = "https://speed.cloudflare.com/__down"
UPLOAD_TEST_URL = "https://speed.cloudflare.com/__up"


@dataclass(frozen=True)
class SpeedTestResult:
    download_mbps: float
    upload_mbps: float
    download_bytes: int
    upload_bytes: int
    download_seconds: float
    upload_seconds: float


def check_internet(
    url: str = CONNECTIVITY_URL,
    timeout: float = 5.0,
    now: Callable[[], float] = time.monotonic,
) -> tuple[bool, float]:
    """Return (is_up, latency_seconds) based on a lightweight HTTP request."""
    start = now()
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        end = now()
        return True, end - start
    except requests.RequestException:
        end = now()
        return False, end - start


def _measure_transfer_speed(
    *,
    method: str,
    url: str,
    bytes_count: int,
    timeout: float,
    now: Callable[[], float] = time.monotonic,
) -> tuple[float, int, float]:
    start = now()
    if method == "GET":
        with requests.get(url, params={"bytes": bytes_count}, stream=True, timeout=timeout) as response:
            response.raise_for_status()
            received = 0
            for chunk in response.iter_content(chunk_size=65536):
                if not chunk:
                    continue
                received += len(chunk)
                if received >= bytes_count:
                    break
    elif method == "POST":
        payload = b"x" * bytes_count
        response = requests.post(url, data=payload, timeout=timeout)
        response.raise_for_status()
        received = bytes_count
    else:
        raise ValueError(f"Unsupported method: {method}")
    end = now()
    duration = max(end - start, 1e-6)
    mbps = (received * 8) / duration / 1_000_000
    return mbps, received, duration


def run_speed_test(
    download_bytes: int = 5_000_000,
    upload_bytes: int = 1_000_000,
    timeout: float = 30.0,
    now: Callable[[], float] = time.monotonic,
) -> SpeedTestResult:
    """Run a basic speed test against Cloudflare's speed test endpoints."""
    download_mbps, download_received, download_seconds = _measure_transfer_speed(
        method="GET",
        url=DOWNLOAD_TEST_URL,
        bytes_count=download_bytes,
        timeout=timeout,
        now=now,
    )
    upload_mbps, upload_sent, upload_seconds = _measure_transfer_speed(
        method="POST",
        url=UPLOAD_TEST_URL,
        bytes_count=upload_bytes,
        timeout=timeout,
        now=now,
    )
    return SpeedTestResult(
        download_mbps=download_mbps,
        upload_mbps=upload_mbps,
        download_bytes=download_received,
        upload_bytes=upload_sent,
        download_seconds=download_seconds,
        upload_seconds=upload_seconds,
    )


def setup_logger(log_path: str) -> logging.Logger:
    logger = logging.getLogger("internet_monitor")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_path)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


def monitor(
    *,
    log_path: str,
    check_interval: int,
    speedtest_interval: int,
    connectivity_url: str = CONNECTIVITY_URL,
    download_bytes: int = 5_000_000,
    upload_bytes: int = 1_000_000,
    run_once: bool = False,
) -> None:
    logger = setup_logger(log_path)
    last_status: bool | None = None
    next_speedtest = time.monotonic()

    while True:
        is_up, latency = check_internet(url=connectivity_url)
        if is_up != last_status:
            status_text = "UP" if is_up else "DOWN"
            logger.info("Connectivity status changed to %s (latency=%.3fs)", status_text, latency)
            last_status = is_up

        current_time = time.monotonic()
        if current_time >= next_speedtest:
            try:
                result = run_speed_test(
                    download_bytes=download_bytes,
                    upload_bytes=upload_bytes,
                )
                logger.info(
                    "Speed test: download=%.2f Mbps (%.2f s), upload=%.2f Mbps (%.2f s)",
                    result.download_mbps,
                    result.download_seconds,
                    result.upload_mbps,
                    result.upload_seconds,
                )
            except requests.RequestException as exc:
                logger.error("Speed test failed: %s", exc)
            next_speedtest = current_time + speedtest_interval

        if run_once:
            break
        time.sleep(check_interval)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Monitor connectivity outages and run periodic speed tests."
    )
    parser.add_argument("--log-path", default="internet_monitor.log")
    parser.add_argument("--check-interval", type=int, default=60, help="Seconds between checks.")
    parser.add_argument(
        "--speedtest-interval",
        type=int,
        default=1800,
        help="Seconds between speed tests (default 30 minutes).",
    )
    parser.add_argument("--connectivity-url", default=CONNECTIVITY_URL)
    parser.add_argument("--download-bytes", type=int, default=5_000_000)
    parser.add_argument("--upload-bytes", type=int, default=1_000_000)
    parser.add_argument("--once", action="store_true", help="Run a single iteration and exit.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    monitor(
        log_path=args.log_path,
        check_interval=args.check_interval,
        speedtest_interval=args.speedtest_interval,
        connectivity_url=args.connectivity_url,
        download_bytes=args.download_bytes,
        upload_bytes=args.upload_bytes,
        run_once=args.once,
    )


if __name__ == "__main__":
    main()
