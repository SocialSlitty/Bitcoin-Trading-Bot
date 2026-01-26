import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd
import matplotlib

# Use Agg backend to avoid GUI issues during tests
matplotlib.use('Agg')

# Add src to path to allow importing bitcoin_sim
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create dummy data for plot_results
        self.df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=100),
            'Close': [100.0] * 100,
            'EMA_7': [100.0] * 100,
            'SMA_30': [100.0] * 100,
            'SMA_200': [100.0] * 100,
            'Volume': [1000.0] * 100,
            'Vol_SMA_10': [1000.0] * 100
        })
        self.trades_log = []

    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.figure') # Mock figure to avoid creating real figures
    def test_plot_results_path_traversal(self, mock_figure, mock_savefig):
        """Test that plot_results raises ValueError for unsafe filenames."""

        # Test parent directory traversal
        with self.assertRaises(ValueError):
            plot_results(self.df, self.trades_log, filename="../plot.png")

        # Test absolute path (should also be rejected to enforce writing to CWD)
        # using /tmp on linux, C:\ on windows (but we simulate logic)
        with self.assertRaises(ValueError):
             plot_results(self.df, self.trades_log, filename="/tmp/plot.png")

        # Test subdirectory
        with self.assertRaises(ValueError):
            plot_results(self.df, self.trades_log, filename="subdir/plot.png")

        # Test backslash
        with self.assertRaises(ValueError):
            plot_results(self.df, self.trades_log, filename="subdir\\plot.png")

    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.figure')
    def test_plot_results_valid_filename(self, mock_figure, mock_savefig):
        """Test that plot_results accepts valid filenames."""

        try:
            plot_results(self.df, self.trades_log, filename="valid_plot.png")
        except ValueError:
            self.fail("plot_results raised ValueError for a valid filename")

        # We assume verify the mock was called if it passed
        mock_savefig.assert_called_with("valid_plot.png")

if __name__ == '__main__':
    unittest.main()
