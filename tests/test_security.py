import unittest
import pandas as pd
import pathlib
import shutil
import os
import tempfile
from src.bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create dummy data for plotting
        self.df = pd.DataFrame({
            "Date": pd.date_range(start="2023-01-01", periods=100),
            "Close": [100.0] * 100,
            "EMA_7": [100.0] * 100,
            "SMA_30": [100.0] * 100,
            "SMA_200": [100.0] * 100,
            "Volume": [1000.0] * 100
        })
        self.trades = []

    def test_path_traversal_prevention(self):
        """Test that plot_results raises ValueError for paths outside CWD."""
        # Create a temporary directory to run this test in isolation
        # This ensures we are "trapped" in a specific CWD
        with tempfile.TemporaryDirectory() as tmpdirname:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdirname)

                # Attempt to write to parent directory
                unsafe_filename = "../evil_plot.png"

                with self.assertRaises(ValueError) as cm:
                    plot_results(self.df, self.trades, filename=unsafe_filename)

                self.assertIn("Security Error", str(cm.exception))
                self.assertIn("outside the working directory", str(cm.exception))

                # Verify file was NOT created in the parent (original_cwd or tmpdirname parent)
                parent_file = pathlib.Path("..").resolve() / "evil_plot.png"
                self.assertFalse(parent_file.exists(), "File should not exist in parent directory")

            finally:
                os.chdir(original_cwd)

    def test_valid_filename(self):
        """Test that a valid filename in CWD works."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdirname)
                valid_filename = "safe_plot.png"

                # Should not raise exception
                plot_results(self.df, self.trades, filename=valid_filename)

                self.assertTrue(os.path.exists(valid_filename))
            finally:
                os.chdir(original_cwd)

if __name__ == "__main__":
    unittest.main()
