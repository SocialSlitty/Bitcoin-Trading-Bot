
import unittest
import sys
import os
import shutil
import pandas as pd
import tempfile
import pathlib

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    """
    Security tests for the Bitcoin Simulator.
    """

    def setUp(self):
        # Mock Data for plotting
        self.df = pd.DataFrame({
            "Date": pd.date_range("2024-01-01", periods=100),
            "Close": [100.0] * 100,
            "EMA_7": [100.0] * 100,
            "SMA_30": [100.0] * 100,
            "SMA_200": [100.0] * 100,
            "Volume": [1000] * 100
        })
        self.trades_log = []

    def test_plot_results_path_traversal_prevention(self):
        """
        Verify that plot_results rejects filenames with path components.
        """
        # 1. Test with simple filename (Allowed)
        # We need to run this in a temp dir to avoid creating junk files
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                # Should not raise
                plot_results(self.df, self.trades_log, filename="test_plot.png")
                self.assertTrue(os.path.exists("test_plot.png"))
            finally:
                os.chdir(original_cwd)

        # 2. Test with directory traversal (Blocked)
        with self.assertRaisesRegex(ValueError, "Filename must not contain path components"):
            plot_results(self.df, self.trades_log, filename="../evil.png")

        # 3. Test with subdirectory (Blocked)
        with self.assertRaisesRegex(ValueError, "Filename must not contain path components"):
            plot_results(self.df, self.trades_log, filename="subdir/evil.png")

        # 4. Test with absolute path (Blocked)
        with self.assertRaisesRegex(ValueError, "Filename must not contain path components"):
             # Use a fake absolute path appropriate for the OS
            if os.name == 'nt':
                abs_path = "C:\\evil.png"
            else:
                abs_path = "/tmp/evil.png"
            plot_results(self.df, self.trades_log, filename=abs_path)

if __name__ == "__main__":
    unittest.main()
