import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):

    @patch('bitcoin_sim.plt')
    def test_plot_results_path_traversal(self, mock_plt):
        """Test that plot_results raises ValueError for filenames with paths."""
        df_mock = MagicMock()
        # Mocking iloc[-60:].copy() chain
        df_mock.iloc.__getitem__.return_value.copy.return_value = df_mock

        trades_log = []

        # Test with a path
        unsafe_filename = "subdir/chart.png"

        with self.assertRaises(ValueError):
            plot_results(df_mock, trades_log, filename=unsafe_filename)

        # Test with parent directory traversal
        with self.assertRaises(ValueError):
             plot_results(df_mock, trades_log, filename="../chart.png")

        # Test with absolute path
        with self.assertRaises(ValueError):
             plot_results(df_mock, trades_log, filename="/tmp/chart.png")

if __name__ == "__main__":
    unittest.main()
