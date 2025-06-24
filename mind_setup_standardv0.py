#!/usr/bin/env python3
import os, shutil, yaml, time, pathlib, argparse, datetime

ROOT = pathlib.Path(os.getenv("MIND_ANCHOR", "~/mind_root")).expanduser()
TRASH = ROOT / ".trash"
CONFIG = ROOT / "config/cleanup.yaml"

parser = argparse.ArgumentParser()
parser.add_argument("--commit", action="store_true", help="wirklich löschen statt Dry‑Run")
args = parser.parse_args()

with open(CONFIG) as f:
    cfg = yaml.safe_load(f)

def should_keep(path):
    from fnmatch import fnmatch
    for pattern in cfg["keep_paths"]:
        if fnmatch(path.relative_to(ROOT).as_posix(), pattern):
            return True
    return False

def should_prune(path):
    from fnmatch import fnmatch
    for pattern in cfg["prune_paths"]:
        if fnmatch(path.relative_to(ROOT).as_posix(), pattern):
            return True
    return False

def aged_out(path):
    days = cfg.get("max_age_days", 30)
    return (time.time() - path.stat().st_mtime) / 86400 > days

def oversize(path):
    mb = cfg.get("max_size_mb", 100)
    return path.stat().st_size / (1024*1024) > mb

for p in ROOT.rglob("*"):
    if p.is_file() and not should_keep(p) and should_prune(p) and (aged_out(p) or oversize(p)):
        print("PRUNE", p)
        if args.commit:
            dst = TRASH / p.relative_to(ROOT)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(p, dst)