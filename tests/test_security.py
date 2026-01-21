import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path to allow importing bitcoin_sim
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import SimConfig, plot_results

class TestSecurity(unittest.TestCase):

    def test_dos_protection_days_limit(self):
        """Test that SimConfig enforces a maximum limit on 'days' to prevent DoS."""
        # This should fail
        with self.assertRaises(ValueError) as cm:
            SimConfig(days=36501)
        self.assertIn("days must be <= 36500", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            SimConfig(days=1_000_000)
        self.assertIn("days must be <= 36500", str(cm.exception))

        # This should pass
        try:
            SimConfig(days=36500)
            SimConfig(days=100)
        except ValueError:
            self.fail("SimConfig raised ValueError for valid days")

    @patch('bitcoin_sim.plt')
    def test_path_traversal_protection(self, mock_plt):
        """Test that plot_results validates the filename to prevent path traversal."""
        # Create dummy data
        import pandas as pd
        df = pd.DataFrame({
            "Date": pd.to_datetime(["2024-01-01"]),
            "Close": [100],
            "EMA_7": [100],
            "SMA_30": [100],
            "SMA_200": [100]
        })
        trades_log = []

        # These should fail
        invalid_filenames = [
            "../evil.png",
            "/tmp/evil.png",
            "dir/test.png",
            r"C:\test.png"
        ]

        for filename in invalid_filenames:
            with self.subTest(filename=filename):
                with self.assertRaises(ValueError) as cm:
                    plot_results(df, trades_log, filename=filename)
                self.assertIn("Filename must not contain path separators", str(cm.exception))

        # These should pass
        valid_filenames = [
            "test.png",
            "simulation_results.png"
        ]

        for filename in valid_filenames:
            try:
                plot_results(df, trades_log, filename=filename)
            except ValueError:
                self.fail(f"plot_results raised ValueError for valid filename: {filename}")

if __name__ == '__main__':
    unittest.main()
