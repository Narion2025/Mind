#!/usr/bin/env python3
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description="Hive cleanup setup")
parser.add_argument("--dry-run", action="store_true", help="run in dry-run mode")
parser.add_argument("--commit", action="store_true", help="apply cleanup")
args = parser.parse_args()

mode = "DRY-RUN" if args.dry_run else "COMMIT" if args.commit else "UNKNOWN"
print(f"[hive_cleanup] {datetime.now().isoformat()} running cleanup in {mode} mode")
