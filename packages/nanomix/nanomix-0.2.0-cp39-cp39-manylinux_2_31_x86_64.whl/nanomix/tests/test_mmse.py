
# Test functions in main.py
import unittest
import os
import sys


script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from main import *
from tools import *

script_dir = os.path.dirname(os.path.realpath(__file__))
methylome = os.path.join(script_dir, 'test_data', 'test_methylome.tsv')
atlas = os.path.join(script_dir, 'test_data', 'test_atlas.tsv')
sigma_path = os.path.join(script_dir, 'test_data', 'test_sigma.tsv')
true_assignments = []

class TestMain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Write sigma
        sigma = [0.3, 0.7]
        coverage = 100
        with open(sigma_path, 'w') as f:
            f.write('cell_type\tproportion\n')
            for i, s in enumerate(sigma):
                f.write(f'cell{i}\t{s}\n')
        # Write an atlas
        with open(atlas, 'w') as f:
            f.write('chr\tstart\tend')
            for i in range(len(sigma)):
                f.write(f'\tcell{i}')
            f.write('\n')
            for i in range(len(sigma)):
                f.write(f'chr1\t{i*100}\t{i*100+99}')
                for j in range(len(sigma)):
                    if i == j:
                        f.write('\t0.99')
                    else:
                        f.write('\t0.01')
                f.write('\n')
        # Simulate a methylome
        with open(methylome, 'w') as f:
            f.write('chromosome\tstart_position\tend_position\ttotal_calls\tmodified_calls\n')
            for i in range(len(sigma)):
                # simulate n reads for every region
                for _ in range(coverage):
                    # choose a cell type wighted by sigma
                    cell_type = np.random.choice(len(sigma), p=sigma)
                    if cell_type == i:
                        f.write(f'chr1\t{i*100}\t{i*100+99}\t1\t1\n')
                    else:
                        f.write(f'chr1\t{i*100}\t{i*100+99}\t1\t0\n')
                    true_assignments.append(f'cell{cell_type}')

    def test_mmse_39Bisulfite(self):
        # initialize the model
        Bisulfite = os.path.join(script_dir, 'test_data/39Bisulfite.tsv')
        sigma = get_sigma_init('null', get_cell_types(Bisulfite))
        model = MMSE(methylome, Bisulfite, sigma, 0, 1)
        # get cell type proportions
        model.optimize(0.0001, 10, 0.01)
        proportions = model.cell_type_proportions()
        correct_proportions = {ct : 1/39 for ct in get_cell_types(Bisulfite)}
        self.assertEqual(proportions, correct_proportions)
    def test_mmse_39Bisulfite_endothelial(self):
        # initialize the model
        Bisulfite = os.path.join(script_dir, 'test_data/39Bisulfite-endothelial.tsv')
        sigma = get_sigma_init('null', get_cell_types(Bisulfite))
        model = MMSE(methylome, Bisulfite, sigma, 0, 1)
        # get cell type proportions
        model.optimize(0.0001, 10, 0.01)
        proportions = model.cell_type_proportions()
        correct_proportions = {ct : 1/42 for ct in get_cell_types(Bisulfite)}
        self.assertEqual(proportions, correct_proportions)



        print(proportions)

if __name__ == '__main__':
    unittest.main()
