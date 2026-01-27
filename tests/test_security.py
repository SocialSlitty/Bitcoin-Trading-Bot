import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import matplotlib
matplotlib.use('Agg')

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    from bitcoin_sim import plot_results, SimConfig
except ImportError:
    # If run from root, this might fail without proper path setup, but sys.path.append handles it.
    pass

class TestSecurity(unittest.TestCase):
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
    def test_plot_results_path_traversal(self, mock_tight_layout, mock_grid, mock_legend, mock_ylabel, mock_xlabel, mock_title, mock_scatter, mock_plot, mock_figure, mock_savefig):
        # Create dummy data
        import pandas as pd
        df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=100),
            'Close': [100.0] * 100,
            'EMA_7': [100.0] * 100,
            'SMA_30': [100.0] * 100,
            'SMA_200': [100.0] * 100
        })
        trades_log = []

        # Test case 1: "../malicious.png"
        filename = "../malicious.png"
        with self.assertRaises(ValueError) as cm:
            plot_results(df, trades_log, filename=filename)

        # We verify the error message is somewhat descriptive
        # Note: The exact message will be implemented in the next step, so we might need to adjust this if the message differs slightly.
        # But generally checking for ValueError is good.
        self.assertTrue("path" in str(cm.exception) or "filename" in str(cm.exception))

        # Test case 2: "..\\malicious.png" (backslash check)
        filename = "..\\malicious.png"
        with self.assertRaises(ValueError) as cm:
            plot_results(df, trades_log, filename=filename)
        self.assertTrue("path" in str(cm.exception) or "filename" in str(cm.exception))

        # Test case 3: Valid filename
        filename = "safe_plot.png"
        plot_results(df, trades_log, filename=filename)
        mock_savefig.assert_called_with(filename)

if __name__ == '__main__':
    unittest.main()
