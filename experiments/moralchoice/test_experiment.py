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

    def test_moralchoice_order_maps_to_underlying_action(self):
        prep = load('experiments/moralchoice/preparation/code/prepare_data.py')
        mapping = prep.mappings()
        choices = {'ab_forward': 'A', 'ab_reverse': 'B', 'repeat_forward': 'first_action', 'repeat_reverse': 'second_action', 'compare_forward': 'yes', 'compare_reverse': 'no'}
        self.assertEqual({mapping[k][v] for k, v in choices.items()}, {'action1'})
        self.assertNotEqual(mapping['compare_forward']['yes'], mapping['compare_reverse']['yes'])
if __name__ == '__main__':
    unittest.main()
