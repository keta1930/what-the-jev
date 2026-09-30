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

    def test_bbq_unknown_failure_and_missing_target_differ(self):
        aggregate = load('experiments/bbq/report/code/metrics.py').aggregate
        base = {'label': 2, 'unknown': 2, 'biased_answer': 0, 'context_condition': 'ambig'}
        rows = [dict(base, prediction=0), dict(base, prediction=1), dict(base, prediction=2), dict(base, prediction=None), dict(base, prediction=0, biased_answer=None)]
        result = aggregate(rows)
        self.assertEqual((result['valid'], result['failed'], result['unknown_count'], result['bias_eligible']), (4, 1, 1, 3))
        self.assertEqual(result['bias_score'], 0)
        self.assertEqual(result['accuracy'], 0.25)
        all_unknown = aggregate([dict(base, prediction=2)])
        self.assertEqual(all_unknown['bias_score'], 0)
        self.assertIsNone(all_unknown['conditional_bias'])
if __name__ == '__main__':
    unittest.main()
