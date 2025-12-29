import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import os
import shutil
from src.bitcoin_sim import plot_results

class TestPlotResultsSecurity(unittest.TestCase):
    def setUp(self):
        # Create dummy data
        dates = pd.date_range(start="2024-01-01", periods=60)
        self.df = pd.DataFrame({
            "Date": dates,
            "Close": np.random.rand(60) * 100,
            "EMA_7": np.random.rand(60) * 100,
            "SMA_30": np.random.rand(60) * 100,
            "SMA_200": np.random.rand(60) * 100
        })
        self.trades_log = []

        # Create a temp subdir to test legal writes
        self.test_dir = Path("test_output")
        self.test_dir.mkdir(exist_ok=True)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        # Cleanup potential files in cwd
        if os.path.exists("legal_test.png"):
            os.remove("legal_test.png")

    def test_path_traversal_absolute(self):
        """Test that absolute paths outside CWD are rejected."""
        filename = "/tmp/should_fail.png"
        with self.assertRaises(ValueError) as cm:
            plot_results(self.df, self.trades_log, filename=filename)
        self.assertIn("Path traversal detected", str(cm.exception))

    def test_path_traversal_relative(self):
        """Test that relative paths attempting to go up are rejected."""
        filename = "../should_fail.png"
        with self.assertRaises(ValueError) as cm:
            plot_results(self.df, self.trades_log, filename=filename)
        self.assertIn("Path traversal detected", str(cm.exception))

    def test_legal_filename(self):
        """Test that a simple filename in CWD is accepted."""
        filename = "legal_test.png"
        try:
            plot_results(self.df, self.trades_log, filename=filename)
        except ValueError:
            self.fail("plot_results raised ValueError unexpectedly for legal filename")
        self.assertTrue(os.path.exists(filename))

    def test_legal_subdirectory(self):
        """Test that a filename in a subdirectory of CWD is accepted."""
        filename = str(self.test_dir / "legal_subdir.png")
        try:
            plot_results(self.df, self.trades_log, filename=filename)
        except ValueError:
            self.fail("plot_results raised ValueError unexpectedly for legal subdirectory")
        self.assertTrue(os.path.exists(filename))

if __name__ == '__main__':
    unittest.main()
