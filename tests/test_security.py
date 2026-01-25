import unittest
import os
import sys
import pandas as pd
import numpy as np
from unittest.mock import patch

# Add src to path to allow importing bitcoin_sim
sys.path.append(os.path.join(os.getcwd(), 'src'))
from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create a dummy dataframe with enough data
        # plot_results uses iloc[-60:], so we need more than 60 rows
        dates = pd.date_range(start='2024-01-01', periods=70)
        self.df = pd.DataFrame({
            'Date': dates,
            'Close': np.random.rand(70) * 1000,
            'EMA_7': np.random.rand(70) * 1000,
            'SMA_30': np.random.rand(70) * 1000,
            'SMA_200': np.random.rand(70) * 1000
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
    @patch('matplotlib.pyplot.gca')
    def test_path_traversal(self, mock_gca, *args):
        # Setup mock_gca to avoid issues
        mock_gca.return_value.get_legend_handles_labels.return_value = ([], [])

        # Test valid filename
        try:
            plot_results(self.df, self.trades_log, filename="safe.png")
        except ValueError:
            self.fail("plot_results raised ValueError unexpectedly for valid filename")

        # Test path traversal
        with self.assertRaises(ValueError, msg="Should raise ValueError for parent directory traversal"):
            plot_results(self.df, self.trades_log, filename="../evil.png")

        with self.assertRaises(ValueError, msg="Should raise ValueError for absolute path"):
            plot_results(self.df, self.trades_log, filename="/tmp/evil.png")

if __name__ == "__main__":
    unittest.main()
