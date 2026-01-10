import sys
import os
import pandas as pd
import numpy as np
import matplotlib
import unittest
import shutil
import tempfile

# Use Agg backend for headless testing
matplotlib.use('Agg')

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestPlotResultsSecurity(unittest.TestCase):
    def setUp(self):
        # Create dummy data
        dates = pd.date_range(start="2023-01-01", periods=100)
        self.df = pd.DataFrame({
            "Date": dates,
            "Close": np.random.rand(100) * 100,
            "EMA_7": np.random.rand(100) * 100,
            "SMA_30": np.random.rand(100) * 100,
            "SMA_200": np.random.rand(100) * 100
        })
        self.trades = []

    def test_path_traversal_prevention(self):
        """Test that plot_results raises ValueError for paths with directories."""
        vulnerable_filenames = [
            "subdir/test.png",
            "/tmp/test.png",
            "../test.png",
            "C:\\test.png" # Even on linux this should be caught if dirname sees it, but maybe not. Let's stick to standard os separators.
        ]

        # We need to test platform specific separators really, but os.path.dirname handles the current OS.
        # Let's test explicit directory injection.

        # Test 1: Simple subdirectory
        with self.assertRaises(ValueError) as cm:
            plot_results(self.df, self.trades, filename=os.path.join("subdir", "test.png"))
        self.assertIn("Security violation", str(cm.exception))

        # Test 2: Absolute path
        with self.assertRaises(ValueError) as cm:
             plot_results(self.df, self.trades, filename=os.path.abspath("test.png"))
        self.assertIn("Security violation", str(cm.exception))

    def test_valid_filename(self):
        """Test that a valid filename allows plotting."""
        valid_filename = "valid_test_plot.png"
        try:
            plot_results(self.df, self.trades, filename=valid_filename)
        except ValueError:
            self.fail("plot_results raised ValueError for a valid filename")

        # Verify file exists
        self.assertTrue(os.path.exists(valid_filename))

        # Cleanup
        if os.path.exists(valid_filename):
            os.remove(valid_filename)

if __name__ == "__main__":
    unittest.main()
