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
        # Create a minimal DataFrame to pass to plot_results
        self.df = pd.DataFrame({
            "Date": pd.date_range("2023-01-01", periods=100),
            "Close": [100.0] * 100,
            "EMA_7": [100.0] * 100,
            "SMA_30": [100.0] * 100,
            "SMA_200": [100.0] * 100
        })
        self.trades = []

    def test_plot_results_path_traversal(self):
        """Test that plot_results rejects filenames with path components."""

        # Test parent directory traversal
        with self.assertRaises(ValueError) as cm:
            plot_results(self.df, self.trades, filename="../evil.png")
        self.assertIn("Path traversal is not allowed", str(cm.exception))

        # Test absolute path
        with self.assertRaises(ValueError) as cm:
            plot_results(self.df, self.trades, filename="/tmp/evil.png")
        self.assertIn("Path traversal is not allowed", str(cm.exception))

        # Test subdirectory
        with self.assertRaises(ValueError) as cm:
            plot_results(self.df, self.trades, filename="subdir/evil.png")
        self.assertIn("Path traversal is not allowed", str(cm.exception))

    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.figure') # Mock figure to avoid creating real plots
    def test_plot_results_valid_filename(self, mock_figure, mock_savefig):
        """Test that plot_results accepts valid filenames."""
        # Should not raise
        plot_results(self.df, self.trades, filename="safe_test_plot.png")

        mock_savefig.assert_called_with("safe_test_plot.png")

if __name__ == "__main__":
    unittest.main()
