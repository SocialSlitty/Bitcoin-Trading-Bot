import unittest
import sys
import os
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

# Add src to path to allow importing bitcoin_sim
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create dummy data for plot_results
        dates = pd.date_range(end="2024-01-01", periods=10)
        self.df = pd.DataFrame({
            "Date": dates,
            "Close": np.random.rand(10) * 100,
            "EMA_7": np.random.rand(10) * 100,
            "SMA_30": np.random.rand(10) * 100,
            "SMA_200": np.random.rand(10) * 100
        })
        self.trades_log = []

    def test_path_traversal_prevention(self):
        """
        Test that plot_results raises a ValueError when a path traversal attempt is made.
        """
        # Attempt to write to parent directory
        malicious_path = "../exploit.png"

        # We expect a ValueError (or similar) to be raised
        with self.assertRaises(ValueError) as cm:
            # We mock plt.savefig to avoid actual file I/O during test,
            # though the security check should happen BEFORE savefig.
            with patch('matplotlib.pyplot.savefig') as mock_savefig:
                plot_results(self.df, self.trades_log, filename=malicious_path)

        self.assertIn("Security violation", str(cm.exception))

    def test_valid_filename(self):
        """
        Test that a valid filename in the current directory works.
        """
        valid_path = "valid_plot.png"

        with patch('matplotlib.pyplot.savefig') as mock_savefig:
            try:
                plot_results(self.df, self.trades_log, filename=valid_path)
            except ValueError:
                self.fail("plot_results raised ValueError for a valid filename")

            mock_savefig.assert_called_once()

    def test_valid_subdirectory(self):
        """
        Test that writing to a valid subdirectory works (if allowed).
        For this implementation, we allow subdirectories as long as they are within CWD.
        """
        # We need to ensure the directory exists or is created, but for the security check logic
        # it just checks path resolving.
        # However, savefig might fail if dir doesn't exist, but that's not a security issue.
        # We mock savefig, so we just test the path validation logic.

        valid_sub_path = "subdir/plot.png"

        with patch('matplotlib.pyplot.savefig') as mock_savefig:
            try:
                plot_results(self.df, self.trades_log, filename=valid_sub_path)
            except ValueError:
                self.fail("plot_results raised ValueError for a valid subdirectory path")

            mock_savefig.assert_called_once()

    def test_absolute_path_outside_cwd(self):
        """
        Test that an absolute path pointing outside CWD is rejected.
        """
        # Construct a path that is definitely outside CWD.
        # In linux, /tmp is usually safe to exist.
        outside_path = "/tmp/exploit.png"

        # If the CWD is /tmp, this test might be invalid.
        # But usually CWD is the repo root.
        if os.getcwd().startswith("/tmp"):
            # Skip if we are running in /tmp
            return

        with self.assertRaises(ValueError) as cm:
            with patch('matplotlib.pyplot.savefig') as mock_savefig:
                plot_results(self.df, self.trades_log, filename=outside_path)

        self.assertIn("Security violation", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
