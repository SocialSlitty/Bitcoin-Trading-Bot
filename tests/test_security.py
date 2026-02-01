import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd

# Add src to path to allow importing bitcoin_sim
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
            "SMA_200": [100] * 100,
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
    def test_plot_results_path_traversal(self, mock_gca, mock_tight_layout, mock_grid,
                                         mock_legend, mock_ylabel, mock_xlabel, mock_title,
                                         mock_scatter, mock_plot, mock_figure, mock_savefig):
        # Setup mock for gca to avoid errors
        mock_gca.return_value.get_legend_handles_labels.return_value = ([], [])

        # Test absolute path
        with self.assertRaisesRegex(ValueError, "Filename must not contain path components"):
            plot_results(self.df, self.trades_log, filename="/tmp/pwned.png")

        # Test relative path traversal
        with self.assertRaisesRegex(ValueError, "Filename must not contain path components"):
            plot_results(self.df, self.trades_log, filename="../pwned.png")

        # Test valid filename
        plot_results(self.df, self.trades_log, filename="valid_plot.png")
        mock_savefig.assert_called_with("valid_plot.png")

if __name__ == "__main__":
    unittest.main()
