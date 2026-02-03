import unittest
import sys
import os
import matplotlib
# Use Agg backend to prevent GUI errors in headless environment
matplotlib.use('Agg')

import pandas as pd
from unittest.mock import patch, MagicMock

# Add src to path to allow importing bitcoin_sim
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):

    def setUp(self):
        # Create a dummy DataFrame and trades_log for testing
        self.df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=100),
            'Close': [100] * 100,
            'EMA_7': [100] * 100,
            'SMA_30': [100] * 100,
            'SMA_200': [100] * 100,
        })
        self.trades_log = []

    @patch('bitcoin_sim.plt')
    @patch('bitcoin_sim.logger')
    def test_plot_results_valid_filename(self, mock_logger, mock_plt):
        # This should pass
        plot_results(self.df, self.trades_log, "valid_filename.png")

        # Verify savefig was called
        mock_plt.savefig.assert_called_with("valid_filename.png")

    @patch('bitcoin_sim.plt')
    @patch('bitcoin_sim.logger')
    def test_plot_results_path_traversal(self, mock_logger, mock_plt):
        # This should fail with ValueError once fixed

        # Testing directory traversal
        with self.assertRaises(ValueError):
            plot_results(self.df, self.trades_log, "../hack.png")

        # Testing absolute path
        with self.assertRaises(ValueError):
            plot_results(self.df, self.trades_log, "/tmp/hack.png")

if __name__ == '__main__':
    unittest.main()
