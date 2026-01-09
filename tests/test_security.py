import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

# We need to ensure we can import bitcoin_sim even if we don't have a display
import matplotlib
matplotlib.use('Agg')

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create dummy data for plot_results
        dates = pd.date_range(start="2023-01-01", periods=100)
        self.df = pd.DataFrame({
            "Date": dates,
            "Close": np.random.rand(100) * 100,
            "EMA_7": np.random.rand(100) * 100,
            "SMA_30": np.random.rand(100) * 100,
            "SMA_200": np.random.rand(100) * 100,
        })
        self.trades = [
            {"Date": "2023-01-10", "Type": "BUY", "Price": 50},
            {"Date": "2023-02-10", "Type": "SELL", "Price": 60}
        ]

    @patch('matplotlib.pyplot.savefig')
    def test_path_traversal_prevention(self, mock_savefig):
        """
        Test that path traversal attempts raise a ValueError.
        """
        dangerous_filenames = [
            "../evil_plot.png",
            "/tmp/evil_plot.png",
            "subdir/evil_plot.png",
            "..\\evil_plot.png" # Windows style
        ]

        for filename in dangerous_filenames:
            # We need to handle os-specific separators for the check
            # Since we are on Linux, backslash might be treated as part of filename,
            # but basename behavior depends on OS.
            # python's os.path.basename handles the separator of the current OS.

            # For this test, let's focus on what is definitely a path separator in this environment
            if os.path.sep in filename:
                with self.subTest(filename=filename):
                    with self.assertRaisesRegex(ValueError, "Path traversal is not allowed"):
                        plot_results(self.df, self.trades, filename=filename)

    @patch('matplotlib.pyplot.savefig')
    def test_valid_filename(self, mock_savefig):
        """
        Test that a valid filename is accepted.
        """
        valid_filename = "safe_plot.png"
        plot_results(self.df, self.trades, filename=valid_filename)
        mock_savefig.assert_called_with(valid_filename)

if __name__ == "__main__":
    unittest.main()
