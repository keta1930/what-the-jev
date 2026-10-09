"""Thin local CLI for the recorded game family."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'src'))
from game_theory.cli import main

if __name__=='__main__':
    try: main()
    except (ValueError,OSError) as exc:
        print('Error: '+str(exc),file=sys.stderr)
        sys.exit(2)
