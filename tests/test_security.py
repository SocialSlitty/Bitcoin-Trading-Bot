import unittest
import sys
import os
import pandas as pd
from unittest.mock import patch

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create dummy data for plot_results
        self.df = pd.DataFrame({
            "Date": pd.date_range(start="2023-01-01", periods=100),
            "Close": [100.0] * 100,
            "EMA_7": [100.0] * 100,
            "SMA_30": [100.0] * 100,
            "SMA_200": [100.0] * 100,
        })
        self.trades_log = []

    @patch('matplotlib.pyplot.savefig')
    def test_path_traversal_prevention(self, mock_savefig):
        """
        Test that plot_results now raises ValueError for paths with components.
        """
        # Test with parent directory traversal
        with self.assertRaisesRegex(ValueError, "Invalid filename:.*Path components are not allowed"):
            plot_results(self.df, self.trades_log, filename="../malicious_plot.png")

        # Test with subdirectory
        with self.assertRaisesRegex(ValueError, "Invalid filename:.*Path components are not allowed"):
            plot_results(self.df, self.trades_log, filename="subdir/malicious_plot.png")

        # Test with absolute path
        with self.assertRaisesRegex(ValueError, "Invalid filename:.*Path components are not allowed"):
            plot_results(self.df, self.trades_log, filename="/tmp/malicious_plot.png")

        # Verify savefig was NOT called
        mock_savefig.assert_not_called()

    @patch('matplotlib.pyplot.savefig')
    def test_valid_filename(self, mock_savefig):
        """
        Test that a valid filename is accepted.
        """
        valid_filename = "valid_plot.png"
        plot_results(self.df, self.trades_log, filename=valid_filename)
        mock_savefig.assert_called_with(valid_filename)

if __name__ == "__main__":
    unittest.main()
