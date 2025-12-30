import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create dummy data for plot_results
        self.df = pd.DataFrame({
            "Date": pd.date_range(start="2023-01-01", periods=100),
            "Close": [100] * 100,
            "EMA_7": [100] * 100,
            "SMA_30": [100] * 100,
            "SMA_200": [100] * 100
        })
        self.trades_log = []

    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.plot')
    @patch('matplotlib.pyplot.scatter')
    @patch('matplotlib.pyplot.title')
    @patch('matplotlib.pyplot.xlabel')
    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.legend')
    @patch('matplotlib.pyplot.grid')
    @patch('matplotlib.pyplot.tight_layout')
    def test_path_traversal_prevention(self, mock_tight, mock_grid, mock_leg, mock_ylab, mock_xlab, mock_title, mock_scat, mock_plot, mock_fig, mock_save):
        # Attempt to write to a parent directory
        unsafe_filename = "../evil_plot.png"

        # We expect a ValueError to be raised when security is implemented.
        # Before the fix, this test should fail because no exception is raised.
        with self.assertRaises(ValueError):
            plot_results(self.df, self.trades_log, filename=unsafe_filename)

if __name__ == "__main__":
    unittest.main()
