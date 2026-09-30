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

    def test_moca_boundaries_are_inclusive_ambiguous(self):
        label = load('experiments/moca/report/code/analyze.py').label3
        self.assertEqual([label(x) for x in [0.399, 0.4, 0.5, 0.6, 0.601]], ['No', 'Ambiguous', 'Ambiguous', 'Ambiguous', 'Yes'])

    def test_release_check_catches_ignored_sources(self):
        audit = load('experiments/moca/verify.py')
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / 'data').mkdir()
            (p / 'data/dataset.json').write_text('{}')
            self.assertEqual(audit.restricted_paths(p), [p / 'data/dataset.json'])
if __name__ == '__main__':
    unittest.main()
