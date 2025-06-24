import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

DEFAULT_ANCHOR = Path.home() / 'mind_root'


def get_anchor() -> Path:
    anchor_env = os.environ.get('MIND_ANCHOR')
    anchor = Path(anchor_env) if anchor_env else DEFAULT_ANCHOR
    try:
        anchor.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f'Fehler beim Erstellen des Anchor-Verzeichnisses {anchor}: {e}')
        raise
    return anchor


def ensure_directories(anchor: Path) -> bool:
    required = [anchor / 'MIND', anchor / 'SKK_OUT']
    tasks_dir = required[0] / 'tasks'
    required.append(tasks_dir)
    created_any = False
    for d in required:
        if not d.exists():
            try:
                d.mkdir(parents=True, exist_ok=True)
                created_any = True
            except Exception as e:
                logger.error(f'Fehler beim Anlegen des Verzeichnisses {d}: {e}')
                raise
    return created_any


def start_scheduler_stub():
    # Platzhalter für Cronjobs oder Scheduler
    logger.info('Scheduler gestartet (Stub)')


def main():
    anchor = get_anchor()
    created = ensure_directories(anchor)
    status = 'Setup-neu' if created else 'Setup-bestehend'
    logger.info('\U0001F9E0 %s' % status)
    start_scheduler_stub()


if __name__ == '__main__':
    main()
