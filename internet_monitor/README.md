# Internet Monitor

This script checks for internet outages and runs periodic speed tests (default every
30 minutes). Speed testing uses Cloudflare's public speed test endpoints.

## Usage

```bash
python -m internet_monitor.monitor --log-path internet_monitor.log
```

Options:

- `--check-interval` seconds between connectivity checks (default 60).
- `--speedtest-interval` seconds between speed tests (default 1800).
- `--once` run one loop iteration and exit (useful for testing).

## Log output

The log file will include connectivity state changes and speed test results, for example:

```
2024-01-01 00:00:00,000 | INFO | Connectivity status changed to DOWN (latency=0.120s)
2024-01-01 00:30:00,000 | INFO | Speed test: download=95.2 Mbps (0.52 s), upload=12.4 Mbps (0.20 s)
```
