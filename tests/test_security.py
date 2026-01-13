import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

# We need to ensure matplotlib backend is Agg before importing pyplot potentially
import matplotlib
matplotlib.use('Agg')

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create minimal dummy data
        self.df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=100),
            'Close': [100.0] * 100,
            'EMA_7': [100.0] * 100,
            'SMA_30': [100.0] * 100,
            'SMA_200': [100.0] * 100,
        })
        self.trades = []

    @patch('bitcoin_sim.plt')
    def test_plot_results_path_traversal(self, mock_plt):
        # Should pass
        plot_results(self.df, self.trades, filename="safe.png")
        mock_plt.savefig.assert_called_with("safe.png")

        # Should fail
        with self.assertRaisesRegex(ValueError, "Filename must be a simple filename"):
            plot_results(self.df, self.trades, filename="../unsafe.png")

        with self.assertRaisesRegex(ValueError, "Filename must be a simple filename"):
            plot_results(self.df, self.trades, filename="/tmp/unsafe.png")

        with self.assertRaisesRegex(ValueError, "Filename must be a simple filename"):
            plot_results(self.df, self.trades, filename="subdir/unsafe.png")

if __name__ == '__main__':
    unittest.main()
