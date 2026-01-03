
import unittest
import pandas as pd
import os
import shutil
from pathlib import Path
import tempfile
from src.bitcoin_sim import plot_results

class TestPlotSecurity(unittest.TestCase):
    def setUp(self):
        # Create dummy data
        dates = pd.date_range(end="2024-12-21", periods=60)
        self.df = pd.DataFrame({
            "Date": dates,
            "Close": [100.0] * 60,
            "EMA_7": [100.0] * 60,
            "SMA_30": [100.0] * 60,
            "SMA_200": [100.0] * 60
        })
        self.trades_log = []

    def test_valid_filename_in_cwd(self):
        """Test writing to a valid filename in the current directory."""
        filename = "valid_security_test.png"
        try:
            plot_results(self.df, self.trades_log, filename=filename)
            self.assertTrue(os.path.exists(filename))
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_valid_relative_path_in_cwd(self):
        """Test writing to a subdirectory in CWD."""
        subdir = Path("subdir_test")
        subdir.mkdir(exist_ok=True)
        filename = str(subdir / "plot.png")
        try:
            plot_results(self.df, self.trades_log, filename=filename)
            self.assertTrue(os.path.exists(filename))
        finally:
            if os.path.exists(filename):
                os.remove(filename)
            if subdir.exists():
                subdir.rmdir()

    def test_path_traversal_prevention(self):
        """Test that writing outside CWD raises a ValueError."""
        # Attempt to write to a temp directory (which is definitely outside CWD)
        with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
            target_path = tmp.name

        # We expect a ValueError
        with self.assertRaises(ValueError) as context:
            plot_results(self.df, self.trades_log, filename=target_path)

        self.assertIn("Security Error", str(context.exception))
        self.assertIn("points outside the current working directory", str(context.exception))

if __name__ == "__main__":
    unittest.main()
