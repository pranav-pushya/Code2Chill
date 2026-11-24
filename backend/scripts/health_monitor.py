"""Code2Chill operations health monitor probe.

Validates service availability, database connectivity and query latency,
and reports operational health metrics in human-readable or JSON format.
"""

import argparse
import json
import os
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# Add backend directory to sys.path so app imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import database_engine


def probe_api_health(base_url: str, timeout_seconds: float = 5.0) -> dict[str, object]:
    url = f"{base_url.rstrip('/')}/api/health"
    start = time.perf_counter()
    req = Request(url, headers={"User-Agent": "Code2Chill-OpsMonitor/1.0"})
    try:
        with urlopen(req, timeout=timeout_seconds) as resp:
            elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "status": "ok" if resp.status == 200 else "degraded",
                "http_status": resp.status,
                "latency_ms": elapsed_ms,
                "data": data,
            }
    except HTTPError as exc:
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        return {
            "status": "down",
            "http_status": exc.code,
            "latency_ms": elapsed_ms,
            "error": exc.reason,
        }
    except URLError as exc:
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        return {
            "status": "unreachable",
            "http_status": None,
            "latency_ms": elapsed_ms,
            "error": str(exc.reason),
        }


def probe_database_direct() -> dict[str, object]:
    start = time.perf_counter()
    try:
        engine = database_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        engine.dispose()
        return {
            "status": "healthy",
            "latency_ms": elapsed_ms,
        }
    except (SQLAlchemyError, RuntimeError, OSError) as exc:
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        return {
            "status": "unavailable",
            "latency_ms": elapsed_ms,
            "error": type(exc).__name__,
        }


def check_all(base_url: str | None = None) -> dict[str, object]:
    target_url = base_url or os.environ.get("PUBLIC_SITE_URL") or "http://127.0.0.1:8000"
    api_result = probe_api_health(target_url)
    db_result = probe_database_direct()

    overall = "healthy"
    if api_result["status"] != "ok" or db_result["status"] != "healthy":
        overall = "degraded" if api_result["status"] == "ok" or db_result["status"] == "healthy" else "down"

    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "overall_status": overall,
        "api": api_result,
        "database": db_result,
    }


def main():
    parser = argparse.ArgumentParser(description="Code2Chill Operations Health Monitor")
    parser.add_argument("--url", default=None, help="Base URL of the API to probe (default: http://127.0.0.1:8000)")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    args = parser.parse_args()
    report = check_all(args.url)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("=== Code2Chill Service Health Report ===")
        print(f"Timestamp:       {report['timestamp']}")
        print(f"Overall Status:  {report['overall_status'].upper()}")
        print(f"API Endpoint:    {report['api']['status'].upper()} (Latency: {report['api']['latency_ms']}ms)")
        print(f"Database Direct: {report['database']['status'].upper()} (Latency: {report['database']['latency_ms']}ms)")

    sys.exit(0 if report["overall_status"] == "healthy" else 1)


if __name__ == "__main__":
    main()
