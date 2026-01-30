import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd

# Add src to path to allow importing bitcoin_sim
sys.path.append(os.path.join(os.getcwd(), 'src'))

# We need to mock matplotlib.pyplot BEFORE importing bitcoin_sim if we wanted to prevent it from loading,
# but since we are patching it inside the test, it's fine.
# However, if bitcoin_sim executes code at top level that uses plt, we might have issues.
# Looking at bitcoin_sim.py, it imports plt but doesn't use it at top level.
# EXCEPT: it sets up logging.

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create a dummy DataFrame
        self.df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=100),
            'Close': [100.0] * 100,
            'EMA_7': [100.0] * 100,
            'SMA_30': [100.0] * 100,
            'SMA_200': [100.0] * 100,
        })
        self.trades_log = []

    @patch('bitcoin_sim.plt')
    def test_path_traversal(self, mock_plt):
        # Test that providing a path with directory separators raises a ValueError

        # We also need to mock os.path.basename checks if we were testing the impl,
        # but here we are testing the public API.

        # Note: We need to check both forward and backward slashes to be thorough,
        # although on Linux backward slash might be a valid filename char.
        # But standard security practice is to deny both.

        filenames = [
            "../evil.png",
            "/tmp/evil.png",
            "subdir/evil.png"
        ]

        for filename in filenames:
            with self.subTest(filename=filename):
                with self.assertRaises(ValueError):
                    plot_results(self.df, self.trades_log, filename=filename)

if __name__ == "__main__":
    unittest.main()
