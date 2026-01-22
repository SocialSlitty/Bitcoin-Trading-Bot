import unittest
import sys
import os
from unittest.mock import patch
import pandas as pd

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "Date": pd.to_datetime(["2023-01-01", "2023-01-02"]),
            "Close": [100, 101],
            "EMA_7": [100, 101],
            "SMA_30": [100, 101],
            "SMA_200": [100, 101]
        })
        self.trades = []

    @patch('bitcoin_sim.plt')
    def test_plot_results_path_traversal(self, mock_plt):
        """Test that plot_results raises ValueError for filenames with path traversal."""
        # Attack payloads
        bad_filenames = [
            "../pwned.png",
            "/tmp/pwned.png",
            "subdir/pwned.png",
            "..\\windows_pwned.png"
        ]

        for bad_filename in bad_filenames:
            with self.subTest(filename=bad_filename):
                with self.assertRaises(ValueError) as cm:
                    plot_results(self.df, self.trades, filename=bad_filename)

                # Check for generic secure error message
                self.assertIn("Filename must not contain path components", str(cm.exception))

    @patch('bitcoin_sim.plt')
    def test_plot_results_valid_filename(self, mock_plt):
        """Test that plot_results accepts valid filenames."""
        # Should not raise
        plot_results(self.df, self.trades, filename="safe.png")
