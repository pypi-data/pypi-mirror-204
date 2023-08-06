import sys
import unittest

import pandas as pd

from PyMolDesc.remove_salt import remove_salt

sys.path.append('..')


class RemoveSaltTestCase(unittest.TestCase):
    def test_remove_salt_single(self):
        smiles_with_salt = '[Na+].[Na+].[O-]C([O-])=O'
        self.assertEqual(remove_salt(smiles_with_salt), 'O=C([O-])[O-]')

    def test_remove_salt_from_file(self):
        smiles_df = pd.read_csv('smiles.csv')['Smiles']
        smiles_without_salt_df = pd.read_csv('smiles_without_salt.csv')['Smiles']

        smiles_processed = smiles_df.apply(remove_salt)
        self.assertEqual(smiles_processed.equals(smiles_without_salt_df), True)


if __name__ == '__main__':
    unittest.main()
