import unittest
import sys
import os
import matplotlib
# Use Agg backend for headless testing
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import SimConfig, plot_results

class TestSecurity(unittest.TestCase):
    def test_dos_protection_days_limit(self):
        """Test that SimConfig rejects excessively large 'days' values to prevent DoS."""
        # Attempt to create a config with 1 billion days.
        # This should raise a ValueError to prevent memory exhaustion.
        with self.assertRaises(ValueError, msg="Should raise ValueError for excessive days"):
            SimConfig(days=1_000_000_000)

    def test_path_traversal_protection(self):
        """Test that plot_results rejects filenames with path traversal characters."""
        df_mock = MagicMock()
        # Mock dataframe columns to prevent KeyError if plot_results accesses them before savefig
        # plot_results uses: Date, Close, EMA_7, SMA_30, SMA_200
        df_mock.iloc.__getitem__.return_value.copy.return_value = df_mock
        df_mock.__getitem__.return_value = [0] * 60 # Mock data

        trades_mock = []

        # We expect validation to prevent paths with separators
        with patch('matplotlib.pyplot.savefig') as mock_save:
             with patch('matplotlib.pyplot.figure'): # Mock figure to speed up
                 with patch('matplotlib.pyplot.plot'):
                     with self.assertRaises(ValueError, msg="Should raise ValueError for path traversal"):
                         plot_results(df_mock, trades_mock, filename="../evil.png")

                     with self.assertRaises(ValueError, msg="Should raise ValueError for absolute path"):
                         plot_results(df_mock, trades_mock, filename="/tmp/evil.png")

if __name__ == '__main__':
    unittest.main()
