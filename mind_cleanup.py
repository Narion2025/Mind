#!/usr/bin/env python3
"""
Einfacher Drive-Cleanup:
  1. Durchläuft alle Mount-Punkte in /proc/mounts (außer tmpfs).
  2. Löscht nur, was älter/größer ist UND nicht auf der Whitelist steht.
  3. Standard: Dry-Run – nichts wird entfernt, nur geloggt.
     Mit --commit werden die Dateien in ~/.trash/ verschoben.
"""
import os, shutil, time, argparse, pathlib, yaml

ROOT      = pathlib.Path(os.getenv("MIND_ANCHOR", "~/mind_root")).expanduser()
TRASH     = pathlib.Path(os.getenv("HOME")) / ".trash"
CONFIG    = ROOT / "config/cleanup.yaml"
MAX_AGE   = 30   # Tage
MAX_SIZE  = 100  # MB

def load_cfg():
    if CONFIG.exists():
        with open(CONFIG) as f:
            return yaml.safe_load(f)
    # Fallback-Whitelist
    return {"keep_globs": ["MIND/**", "config/**", "*.sh"]}

def iter_drives():
    with open("/proc/mounts") as f:
        for line in f:
            dev, mnt, fstype, *_ = line.split()
            if fstype == "tmpfs":   # temporäre RAM-Disks überspringen
                continue
            yield pathlib.Path(mnt)

def whitelisted(path, globs):
    from fnmatch import fnmatch
    rel = path.as_posix()
    return any(fnmatch(rel, g) for g in globs)

def aged_out(p):
    return (time.time() - p.stat().st_mtime) / 86400 > MAX_AGE

def oversize(p):
    return p.stat().st_size / (1024*1024) > MAX_SIZE

def main(commit=False):
    cfg = load_cfg()
    keep = cfg["keep_globs"]
    TRASH.mkdir(exist_ok=True)

    for drive in iter_drives():
        for p in drive.rglob("*"):
            if p.is_file() and not whitelisted(p, keep) and (aged_out(p) or oversize(p)):
                action = "DELETE" if commit else "CANDIDATE"
                print(f"{action}: {p}")
                if commit:
                    dst = TRASH / p.relative_to("/")
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(p, dst)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", action="store_true")
    main(ap.parse_args().commit)
