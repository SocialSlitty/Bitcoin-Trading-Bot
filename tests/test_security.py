import unittest
import sys
import os
import pandas as pd
import numpy as np
import matplotlib

# Set backend to Agg before importing pyplot
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create minimal valid data for plot_results
        dates = pd.date_range(start="2024-01-01", periods=100)
        self.df = pd.DataFrame({
            "Date": dates,
            "Close": np.random.rand(100) * 100,
            "EMA_7": np.random.rand(100) * 100,
            "SMA_30": np.random.rand(100) * 100,
            "SMA_200": np.random.rand(100) * 100
        })
        self.trades = []

    def test_path_traversal_prevention(self):
        """Test that plot_results rejects filenames with directory traversal components."""

        # Test parent directory traversal
        with self.assertRaises(ValueError):
            plot_results(self.df, self.trades, filename="../evil_plot.png")

        # Test absolute path (should likely be rejected too to enforce current working dir,
        # or we just strictly check for no slashes)
        # For this fix, I'll enforce no path separators at all.
        with self.assertRaises(ValueError):
            plot_results(self.df, self.trades, filename="/tmp/evil_plot.png")

        # Test valid filename should pass (we mock savefig to avoid actual file IO)
        with patch('matplotlib.pyplot.savefig') as mock_savefig:
            plot_results(self.df, self.trades, filename="safe_plot.png")
            mock_savefig.assert_called_once_with("safe_plot.png")

if __name__ == "__main__":
    unittest.main()
