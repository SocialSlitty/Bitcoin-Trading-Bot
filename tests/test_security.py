import unittest
import sys
import os
import unittest.mock as mock
import pandas as pd
import matplotlib

# Use Agg backend to prevent display errors
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create minimal mock data
        dates = pd.date_range(start="2023-01-01", periods=60)
        self.df = pd.DataFrame({
            "Date": dates,
            "Close": [100.0] * 60,
            "EMA_7": [100.0] * 60,
            "SMA_30": [100.0] * 60,
            "SMA_200": [100.0] * 60
        })
        self.trades_log = []

    @mock.patch('matplotlib.pyplot.savefig')
    @mock.patch('matplotlib.pyplot.figure')
    @mock.patch('matplotlib.pyplot.plot')
    @mock.patch('matplotlib.pyplot.scatter')
    @mock.patch('matplotlib.pyplot.title')
    @mock.patch('matplotlib.pyplot.xlabel')
    @mock.patch('matplotlib.pyplot.ylabel')
    @mock.patch('matplotlib.pyplot.legend')
    @mock.patch('matplotlib.pyplot.grid')
    @mock.patch('matplotlib.pyplot.tight_layout')
    @mock.patch('matplotlib.pyplot.gca')
    def test_plot_results_path_traversal(self, *args):
        # Should raise ValueError for parent directory
        with self.assertRaisesRegex(ValueError, "Path components are not allowed"):
            plot_results(self.df, self.trades_log, filename="../plot.png")

        # Should raise ValueError for subdirectory
        with self.assertRaisesRegex(ValueError, "Path components are not allowed"):
            plot_results(self.df, self.trades_log, filename="subdir/plot.png")

        # Should raise ValueError for absolute path
        with self.assertRaisesRegex(ValueError, "Path components are not allowed"):
            plot_results(self.df, self.trades_log, filename="/tmp/plot.png")

    @mock.patch('matplotlib.pyplot.savefig')
    @mock.patch('matplotlib.pyplot.figure')
    @mock.patch('matplotlib.pyplot.plot')
    @mock.patch('matplotlib.pyplot.scatter')
    @mock.patch('matplotlib.pyplot.title')
    @mock.patch('matplotlib.pyplot.xlabel')
    @mock.patch('matplotlib.pyplot.ylabel')
    @mock.patch('matplotlib.pyplot.legend')
    @mock.patch('matplotlib.pyplot.grid')
    @mock.patch('matplotlib.pyplot.tight_layout')
    @mock.patch('matplotlib.pyplot.gca')
    def test_plot_results_valid_filename(self, mock_gca, mock_tight, mock_grid, mock_legend, mock_ylabel, mock_xlabel, mock_title, mock_scatter, mock_plot, mock_fig, mock_savefig):
        # Setup mock gca to return a mock with get_legend_handles_labels
        # It returns (handles, labels)
        mock_gca.return_value.get_legend_handles_labels.return_value = ([], [])

        # Valid filename should not raise
        plot_results(self.df, self.trades_log, filename="valid_plot.png")
        mock_savefig.assert_called_with("valid_plot.png")

if __name__ == "__main__":
    unittest.main()
