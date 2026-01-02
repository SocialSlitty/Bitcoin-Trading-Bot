import unittest
import tempfile
import os
import pandas as pd
from src.bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create dummy data for plotting
        dates = pd.date_range(start="2024-01-01", periods=100)
        self.df = pd.DataFrame({
            "Date": dates,
            "Close": [100] * 100,
            "EMA_7": [100] * 100,
            "SMA_30": [100] * 100,
            "SMA_200": [100] * 100
        })
        self.trades_log = []

    def test_path_traversal_protection(self):
        """Test that plot_results raises ValueError for path traversal attempts."""
        # This should fail because it tries to write to the parent directory
        # or a directory outside the current working directory.

        # We need to be careful here. The function checks against os.getcwd().
        # So passing "../something" should trigger it.

        with self.assertRaises(ValueError) as cm:
            plot_results(self.df, self.trades_log, filename="../traversal_attempt.png")

        self.assertIn("Security Error", str(cm.exception))
        self.assertIn("Output must be within the current working directory", str(cm.exception))

    def test_valid_path(self):
        """Test that plot_results works for valid paths in current directory."""
        # Using a temporary file name in the current directory
        # We cannot use tempfile.NamedTemporaryFile because plot_results expects to create the file,
        # and checking strict containment in CWD might fail if temp dir is elsewhere (e.g. /tmp).
        # But we can verify it works for a local file.

        filename = "valid_plot_test.png"

        # Ensure it doesn't exist
        if os.path.exists(filename):
            os.remove(filename)

        try:
            plot_results(self.df, self.trades_log, filename=filename)
            self.assertTrue(os.path.exists(filename))
        finally:
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == "__main__":
    unittest.main()
