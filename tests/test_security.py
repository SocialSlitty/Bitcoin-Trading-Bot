import unittest
import os
import sys
import matplotlib
matplotlib.use('Agg')
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from bitcoin_sim import SimConfig, plot_results

class TestSecurity(unittest.TestCase):
    def test_sim_config_dos_protection(self):
        """Test that SimConfig rejects excessive days to prevent DoS."""
        # Valid days
        config = SimConfig(days=365)
        self.assertEqual(config.days, 365)

        # Invalid days (DoS)
        with self.assertRaises(ValueError) as cm:
            SimConfig(days=100000)
        self.assertIn("days must be", str(cm.exception))

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
    def test_plot_results_path_traversal(self, mock_tight, mock_grid, mock_leg, mock_ylab, mock_xlab, mock_title, mock_scat, mock_plot, mock_fig, mock_savefig):
        """Test that plot_results rejects filenames with path traversal."""
        # Mock dataframe behavior needed for plot_results
        import pandas as pd
        df = pd.DataFrame({
            "Date": pd.date_range("2023-01-01", periods=100),
            "Close": [100]*100,
            "EMA_7": [100]*100,
            "SMA_30": [100]*100,
            "SMA_200": [100]*100
        })
        trades = []

        # Valid filename
        plot_results(df, trades, filename="safe_plot.png")
        mock_savefig.assert_called_with("safe_plot.png")

        # Invalid filename (Traversal)
        with self.assertRaises(ValueError) as cm:
            plot_results(df, trades, filename="../evil.png")
        self.assertIn("Filename must not contain path components", str(cm.exception))

        # Invalid filename (Absolute path)
        with self.assertRaises(ValueError) as cm:
            plot_results(df, trades, filename="/tmp/evil.png")
        self.assertIn("Filename must not contain path components", str(cm.exception))

        # Invalid filename (Backslash for Windows traversal on Linux? - debatable but good practice)
        # On Linux, backslash is a valid char, but good to ban it to be safe.
        # But if the code uses os.path.split, it might not catch it on Linux.
        # We will strictly enforce "no path separators".

if __name__ == '__main__':
    unittest.main()
