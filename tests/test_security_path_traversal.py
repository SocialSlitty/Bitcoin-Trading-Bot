import unittest
import os
import shutil
import tempfile
import pandas as pd
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend
import matplotlib.pyplot as plt
from src.bitcoin_sim import plot_results

class TestSecurityPathTraversal(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory structure:
        # /tmp/test_run/
        #   cwd/  <-- we will run from here
        #   target/ <-- we try to write here using ..
        self.test_root = tempfile.mkdtemp()
        self.cwd = os.path.join(self.test_root, 'cwd')
        self.target_dir = os.path.join(self.test_root, 'target')
        os.makedirs(self.cwd)
        os.makedirs(self.target_dir)

        # Save original CWD
        self.original_cwd = os.getcwd()
        os.chdir(self.cwd)

        # Create dummy dataframe sufficient for plot_results (needs 60 rows)
        self.df = pd.DataFrame({
            'Date': pd.date_range(start='2021-01-01', periods=100),
            'Close': [100.0 + i for i in range(100)],
            'EMA_7': [100.0 + i for i in range(100)],
            'SMA_30': [100.0 + i for i in range(100)],
            'SMA_200': [100.0 + i for i in range(100)],
        })
        self.trades = []

    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_root)

    def test_path_traversal_prevention(self):
        # Define a path that goes up one level to the target directory
        filename = "../target/hacked.png"
        abs_target_path = os.path.join(self.target_dir, "hacked.png")

        # Verify file doesn't exist yet
        self.assertFalse(os.path.exists(abs_target_path))

        # Call the function - expect ValueError
        with self.assertRaises(ValueError) as context:
            plot_results(self.df, self.trades, filename=filename)

        self.assertIn("Path traversal detected", str(context.exception))

        # Verify the file was NOT created
        self.assertFalse(os.path.exists(abs_target_path), "File created despite security check!")

if __name__ == '__main__':
    unittest.main()
