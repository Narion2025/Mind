#!/usr/bin/env bash
set -e

# Start the Python bootstrap to initialize base directories
python3 mind_bootstrap.py

# ===== Hive Boot Block =====
# 1. SKK-Scheduler Import
echo "[hive_boot] import SKKScheduler …"
python3 - <<'PY'
from tools.skk.skk_autoanalyse_scheduler import SKKScheduler
SKKScheduler().analyze_daily_input("Boot-Test")
PY

# 2. Cleanup Setup Dry Run
mkdir -p logs
python3 tools/hive_cleanup_setup.py --dry-run | tee -a logs/hive_cleanup.log

# 3. Ensure directory structure
mkdir -p tools/skk SKK_OUT config/markers semnet modules thoughts wiki blob logs

# 4. Cron entry for Hive Scheduler
CRON_LINE="0 0 * * * python3 $(pwd)/tools/skk/skk_autoanalyse_scheduler.py --daily"
(crontab -l 2>/dev/null; echo "$CRON_LINE") | sort -u | crontab -

# 5. Hive Resonance Test
curl -X POST http://localhost:8000/task -d '{"agent":"hive_regulator","body":"Test Hive-Resonanz"}' || true

