import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import pandas as pd

# Add src to path to allow importing bitcoin_sim
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    @patch('bitcoin_sim.plt')
    def test_path_traversal_plot_results(self, mock_plt):
        """Test that plot_results raises ValueError for filenames with path traversal."""
        # Create dummy data sufficient for plot_results
        df = pd.DataFrame({
            'Date': [pd.Timestamp('2023-01-01')],
            'Close': [100.0],
            'EMA_7': [100.0],
            'SMA_30': [100.0],
            'SMA_200': [100.0]
        })
        trades = []

        # Test with a path traversal filename
        filename = "parent/evil.png"

        # We expect a ValueError
        with self.assertRaises(ValueError) as cm:
            plot_results(df, trades, filename=filename)

        self.assertIn("path traversal", str(cm.exception).lower())

if __name__ == '__main__':
    unittest.main()
