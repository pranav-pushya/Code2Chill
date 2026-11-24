"""Code2Chill database operations: automated backup, verification, and retention.

Creates timestamped custom-format PostgreSQL dumps, generates SHA-256 checksums,
verifies backup integrity, and enforces retention policies.
"""

import argparse
import hashlib
import os
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import dotenv_values

BACKEND_DIR = Path(__file__).resolve().parents[1]
DEFAULT_BACKUP_DIR = BACKEND_DIR / "backups"
ENV_FILE = BACKEND_DIR / ".env"


def get_db_config() -> dict[str, str]:
    settings = {**dotenv_values(ENV_FILE), **os.environ}
    return {
        "host": settings.get("DB_HOST", "127.0.0.1"),
        "port": settings.get("DB_HOST_PORT", "55432"),
        "user": settings.get("POSTGRES_USER", "code2chill"),
        "database": settings.get("POSTGRES_DB", "code2chill"),
        "password": settings.get("POSTGRES_PASSWORD", ""),
        "retention_days": int(settings.get("BACKUP_RETENTION_DAYS", "14")),
    }


def compute_sha256(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with file_path.open("rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_pg_dump() -> list[str]:
    """Find local pg_dump executable or Docker container fallback."""
    if pg_dump := shutil.which("pg_dump"):
        return [pg_dump]
    container = os.environ.get("RECOVERY_DB_CONTAINER") or os.environ.get("POSTGRES_CONTAINER")
    if container and shutil.which("docker"):
        return ["docker", "exec", container, "pg_dump"]
    return ["pg_dump"]


def create_backup(
    output_dir: Path | None = None,
    retention_days: int | None = None,
) -> tuple[Path, Path]:
    config = get_db_config()
    target_dir = Path(output_dir) if output_dir else DEFAULT_BACKUP_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    days = retention_days if retention_days is not None else config["retention_days"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dump_filename = f"code2chill_{timestamp}.dump"
    dump_path = target_dir / dump_filename
    checksum_path = target_dir / f"{dump_filename}.sha256"

    cmd = [
        *find_pg_dump(),
        "--format=custom",
        "--compress=9",
        f"--host={config['host']}",
        f"--port={config['port']}",
        f"--username={config['user']}",
        f"--dbname={config['database']}",
        f"--file={dump_path}",
    ]

    env = os.environ.copy()
    if config["password"]:
        env["PGPASSWORD"] = config["password"]

    result = subprocess.run(cmd, check=False, env=env, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"pg_dump failed (exit {result.returncode}): {result.stderr.strip()}")

    if not dump_path.is_file() or dump_path.stat().st_size == 0:
        raise RuntimeError(f"Backup file was not created or is empty: {dump_path}")

    # Compute and save SHA-256
    digest = compute_sha256(dump_path)
    checksum_path.write_text(f"{digest}  {dump_filename}\n", encoding="utf-8")

    # Enforce retention policy
    prune_old_backups(target_dir, days)

    return dump_path, checksum_path


def prune_old_backups(backup_dir: Path, retention_days: int) -> list[Path]:
    if retention_days <= 0:
        return []
    cutoff = datetime.now() - timedelta(days=retention_days)
    pruned = []
    for file in backup_dir.glob("code2chill_*.dump*"):
        mtime = datetime.fromtimestamp(file.stat().st_mtime)
        if mtime < cutoff:
            file.unlink(missing_ok=True)
            pruned.append(file)
    return pruned


def verify_backup(dump_path: Path) -> bool:
    if not dump_path.is_file():
        return False
    checksum_file = dump_path.with_suffix(dump_path.suffix + ".sha256")
    if not checksum_file.is_file():
        return False
    expected_hash = checksum_file.read_text(encoding="utf-8").strip().split()[0]
    actual_hash = compute_sha256(dump_path)
    return expected_hash.lower() == actual_hash.lower()


def list_backups(backup_dir: Path | None = None) -> list[dict[str, object]]:
    target_dir = Path(backup_dir) if backup_dir else DEFAULT_BACKUP_DIR
    if not target_dir.is_dir():
        return []
    backups = []
    for dump in sorted(target_dir.glob("code2chill_*.dump"), reverse=True):
        size_bytes = dump.stat().st_size
        created_at = datetime.fromtimestamp(dump.stat().st_mtime).isoformat()
        verified = verify_backup(dump)
        backups.append(
            {
                "file": dump.name,
                "path": str(dump),
                "size_bytes": size_bytes,
                "created_at": created_at,
                "verified": verified,
            }
        )
    return backups


def main():
    parser = argparse.ArgumentParser(description="Code2Chill Database Backup Utility")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_BACKUP_DIR, help="Backup output directory")
    parser.add_argument("--retention-days", type=int, default=None, help="Retention period in days")
    parser.add_argument("--list", action="store_true", help="List existing backups and verification status")
    parser.add_argument("--verify", type=Path, help="Verify SHA-256 checksum of a specific dump file")

    args = parser.parse_args()

    if args.list:
        backups = list_backups(args.output_dir)
        if not backups:
            print("No backups found.")
            return
        print(f"Found {len(backups)} backup(s) in {args.output_dir}:")
        for b in backups:
            status = "VALID" if b["verified"] else "INVALID/MISSING_CHECKSUM"
            print(f"- {b['file']} ({b['size_bytes']:,} bytes, {b['created_at']}) [{status}]")
        return

    if args.verify:
        if verify_backup(args.verify):
            print(f"Backup integrity verified: {args.verify.name}")
        else:
            parser.exit(1, f"Checksum verification failed for: {args.verify}\n")
        return

    dump_path, sha_path = create_backup(args.output_dir, args.retention_days)
    print(f"Backup created: {dump_path.name} ({dump_path.stat().st_size:,} bytes)")
    print(f"Checksum: {sha_path.name}")


if __name__ == "__main__":
    main()
