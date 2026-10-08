"""Start a single-turn decision experiment from a config path."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT / 'src') not in sys.path:
    sys.path.insert(0, str(ROOT / 'src'))

from decision_models.logger import configure_logging  # noqa: E402
from decision_models.runner import run  # noqa: E402

CONFIG = ROOT / 'example/ticket-triage/config.yaml'


def main() -> None:
    """Use CONFIG as it stands, or pass one experiment config path."""
    if len(sys.argv) > 2:
        raise SystemExit('usage: python run.py [config.yaml]')
    configure_logging()
    run(sys.argv[1] if len(sys.argv) == 2 else CONFIG)


if __name__ == '__main__':
    main()
