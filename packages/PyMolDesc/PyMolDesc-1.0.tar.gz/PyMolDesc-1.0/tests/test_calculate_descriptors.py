import sys

import unittest

import pandas as pd

from PyMolDesc.calculate_descriptors import calculate_descriptors, check_lipinski_rules

sys.path.append('..')
sys.path.append('../PyMolDesc/')


class CalculateDescriptorsTestCase(unittest.TestCase):
    @staticmethod
    def test_check_lipinski_rules():
        # Test case 1: all properties within the limit
        row = pd.Series({'ExactMolWt': 249.3, 'MolLogP': 1.4, 'NumHDonors': 1, 'NumHAcceptors': 3})
        assert check_lipinski_rules(row) == 0

        # Test case 2: ExactMolWt above the limit
        row = pd.Series({'ExactMolWt': 501, 'MolLogP': 1.4, 'NumHDonors': 1, 'NumHAcceptors': 3})
        assert check_lipinski_rules(row) == 1

        # Test case 3: MolLogP above the limit
        row = pd.Series({'ExactMolWt': 249.3, 'MolLogP': 6, 'NumHDonors': 1, 'NumHAcceptors': 3})
        assert check_lipinski_rules(row) == 1

        # Test case 4: NumHDonors above the limit
        row = pd.Series({'ExactMolWt': 249.3, 'MolLogP': 1.4, 'NumHDonors': 6, 'NumHAcceptors': 3})
        assert check_lipinski_rules(row) == 1

        # Test case 5: NumHAcceptors above the limit
        row = pd.Series({'ExactMolWt': 249.3, 'MolLogP': 1.4, 'NumHDonors': 1, 'NumHAcceptors': 11})
        assert check_lipinski_rules(row) == 1


if __name__ == '__main__':
    unittest.main()
