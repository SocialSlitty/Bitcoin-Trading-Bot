import unittest
import os
import sys
import matplotlib
# Set backend to Agg before importing pyplot (via bitcoin_sim) to prevent GUI errors in headless env
matplotlib.use('Agg')

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results
import pandas as pd
from unittest.mock import patch

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create a dummy dataframe
        self.df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=100),
            'Close': [100.0] * 100,
            'EMA_7': [100.0] * 100,
            'SMA_30': [100.0] * 100,
            'SMA_200': [100.0] * 100,
            # Add Volume columns required by plot_results if it uses them (it uses Close, EMA_7, SMA_30, SMA_200)
        })
        self.trades_log = []

    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.figure")
    @patch("matplotlib.pyplot.plot")
    @patch("matplotlib.pyplot.scatter")
    @patch("matplotlib.pyplot.title")
    @patch("matplotlib.pyplot.xlabel")
    @patch("matplotlib.pyplot.ylabel")
    @patch("matplotlib.pyplot.legend")
    @patch("matplotlib.pyplot.grid")
    @patch("matplotlib.pyplot.tight_layout")
    def test_plot_results_path_traversal(self, mock_tight_layout, mock_grid, mock_legend, mock_ylabel, mock_xlabel, mock_title, mock_scatter, mock_plot, mock_figure, mock_savefig):
        """
        Test that plot_results raises ValueError when a path with directories is provided.
        This prevents path traversal attacks.
        """
        # Test with a nested path
        nested_path = os.path.join("some_dir", "test_plot.png")

        with self.assertRaises(ValueError) as cm:
            plot_results(self.df, self.trades_log, filename=nested_path)

        self.assertIn("Path components are not allowed", str(cm.exception))

        # Test with parent directory traversal
        traversal_path = os.path.join("..", "test_plot.png")

        with self.assertRaises(ValueError) as cm:
            plot_results(self.df, self.trades_log, filename=traversal_path)

        self.assertIn("Path components are not allowed", str(cm.exception))

        # Verify savefig was NOT called
        mock_savefig.assert_not_called()

    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.figure")
    @patch("matplotlib.pyplot.plot")
    @patch("matplotlib.pyplot.scatter")
    @patch("matplotlib.pyplot.title")
    @patch("matplotlib.pyplot.xlabel")
    @patch("matplotlib.pyplot.ylabel")
    @patch("matplotlib.pyplot.legend")
    @patch("matplotlib.pyplot.grid")
    @patch("matplotlib.pyplot.tight_layout")
    def test_plot_results_valid_filename(self, mock_tight_layout, mock_grid, mock_legend, mock_ylabel, mock_xlabel, mock_title, mock_scatter, mock_plot, mock_figure, mock_savefig):
        """
        Test that plot_results accepts a valid filename.
        """
        valid_filename = "safe_plot.png"
        plot_results(self.df, self.trades_log, filename=valid_filename)

        # Verify savefig was called with the valid filename
        mock_savefig.assert_called_with(valid_filename)

if __name__ == '__main__':
    unittest.main()
