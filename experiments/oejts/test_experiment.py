"""Regression cases for the nontrivial scoring and distribution boundaries."""
from pathlib import Path
import importlib.util
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[2]

def load(relative):
    p = ROOT / relative
    spec = importlib.util.spec_from_file_location(p.parent.name + '_' + p.stem, p)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

class ExperimentTests(unittest.TestCase):

    def test_oejts_neutral_boundary_and_one_step_change(self):
        score = load('experiments/oejts/report/code/analyze.py').score
        neutral = score([3] * 32)
        self.assertEqual(neutral['type'], 'ISFJ')
        self.assertEqual(neutral['scores'], dict.fromkeys(['IE', 'SN', 'FT', 'JP'], 24))
        self.assertEqual(len(neutral['boundary_axes']), 4)
        changed = [3] * 32
        changed[2] = 2
        self.assertEqual(score(changed)['type'], 'ESFJ')

    def test_oejts_rejects_invalid_scale_positions(self):
        score = load('experiments/oejts/report/code/analyze.py').score
        for values in ([3] * 31, [0] + [3] * 31, [6] + [3] * 31, [True] + [3] * 31):
            with self.assertRaises(ValueError):
                score(values)

    def test_release_check_catches_ignored_sources(self):
        audit = load('experiments/oejts/verify.py')
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / 'data').mkdir()
            (p / 'data/dataset.json').write_text('{}')
            self.assertEqual(audit.restricted_paths(p), [p / 'data/dataset.json'])
if __name__ == '__main__':
    unittest.main()
