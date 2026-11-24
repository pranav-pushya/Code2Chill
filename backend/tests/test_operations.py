import hashlib
from datetime import datetime, timedelta
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from scripts.backup import compute_sha256, list_backups, prune_old_backups, verify_backup
from scripts.health_monitor import check_all, probe_database_direct


def test_health_endpoints():
    with TestClient(app) as client:
        # 1. Classic health endpoint
        resp = client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

        # 2. Operations health endpoint with latency & diagnostics
        ops_resp = client.get("/api/health/ops")
        assert ops_resp.status_code == 200
        data = ops_resp.json()
        assert data["status"] == "healthy"
        assert data["services"]["api"] == "ok"
        assert data["services"]["database"] == "healthy"
        assert isinstance(data["database_latency_ms"], (int, float))
        assert data["database_latency_ms"] >= 0


def test_monitor_requests_middleware():
    with TestClient(app) as client:
        # Public content request should complete cleanly
        resp = client.get("/api/site-links")
        assert resp.status_code == 200

        # Non-existent route
        resp_404 = client.get("/api/non-existent-endpoint")
        assert resp_404.status_code == 404


def test_backup_checksum_and_verification(tmp_path: Path):
    dummy_dump = tmp_path / "code2chill_20261124_120000.dump"
    dummy_dump.write_bytes(b"PGDMP_DUMMY_BINARY_DATA_FOR_TESTING_1234567890")

    # Compute sha256
    digest = compute_sha256(dummy_dump)
    expected_digest = hashlib.sha256(b"PGDMP_DUMMY_BINARY_DATA_FOR_TESTING_1234567890").hexdigest()
    assert digest == expected_digest

    # Write checksum file
    sha_file = dummy_dump.with_suffix(".dump.sha256")
    sha_file.write_text(f"{digest}  {dummy_dump.name}\n", encoding="utf-8")

    # Verification should succeed
    assert verify_backup(dummy_dump) is True

    # Corrupt data -> verification should fail
    dummy_dump.write_bytes(b"CORRUPTED_DATA")
    assert verify_backup(dummy_dump) is False


def test_backup_retention_pruning(tmp_path: Path):
    old_dump = tmp_path / "code2chill_20261101_120000.dump"
    old_dump.write_bytes(b"OLD_DUMP")
    old_sha = tmp_path / "code2chill_20261101_120000.dump.sha256"
    old_sha.write_text("dummy old sha", encoding="utf-8")

    fresh_dump = tmp_path / "code2chill_20261124_120000.dump"
    fresh_dump.write_bytes(b"FRESH_DUMP")
    fresh_sha = tmp_path / "code2chill_20261124_120000.dump.sha256"
    fresh_sha.write_text("dummy fresh sha", encoding="utf-8")

    # Set old dump modification time to 30 days ago
    thirty_days_ago = (datetime.now() - timedelta(days=30)).timestamp()
    import os

    os.utime(old_dump, (thirty_days_ago, thirty_days_ago))
    os.utime(old_sha, (thirty_days_ago, thirty_days_ago))

    # Prune with 14-day retention
    pruned = prune_old_backups(tmp_path, retention_days=14)
    assert len(pruned) == 2
    assert old_dump not in tmp_path.iterdir()
    assert old_sha not in tmp_path.iterdir()
    assert fresh_dump.is_file()
    assert fresh_sha.is_file()


def test_list_backups(tmp_path: Path):
    dump_file = tmp_path / "code2chill_20261124_150000.dump"
    dump_file.write_bytes(b"SAMPLE_CONTENT")
    sha_file = tmp_path / "code2chill_20261124_150000.dump.sha256"
    digest = hashlib.sha256(b"SAMPLE_CONTENT").hexdigest()
    sha_file.write_text(f"{digest}  {dump_file.name}\n", encoding="utf-8")

    backups = list_backups(tmp_path)
    assert len(backups) == 1
    assert backups[0]["file"] == dump_file.name
    assert backups[0]["verified"] is True
    assert backups[0]["size_bytes"] == len(b"SAMPLE_CONTENT")


def test_health_monitor_probes():
    db_status = probe_database_direct()
    assert db_status["status"] == "healthy"
    assert "latency_ms" in db_status

    # Probe full check_all
    report = check_all(base_url="http://127.0.0.1:8000")
    assert report["database"]["status"] == "healthy"
    assert "timestamp" in report
