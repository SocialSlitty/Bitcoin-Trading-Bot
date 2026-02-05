import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import pandas as pd

# Configure matplotlib backend before importing pyplot-dependent modules
import matplotlib
matplotlib.use('Agg')

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestPathTraversal(unittest.TestCase):
    @patch('bitcoin_sim.plt')
    def test_path_traversal(self, mock_plt):
        # Create a mock DataFrame
        # plot_results uses: df.iloc[-60:].copy()
        # and then accesses columns like ['Date'], ['Close'] etc.

        mock_df = MagicMock()

        # Setup the chain: df.iloc[-60:].copy() -> final_mock_df
        final_mock_df = MagicMock()

        # When accessing columns on the sliced df, return simple arrays
        # The code does: plt.plot(plot_data["Date"], ...)
        # So __getitem__ needs to return something iterable/plottable
        final_mock_df.__getitem__.return_value = [1, 2, 3]

        # Mock the copy method to return our prepared final_mock_df
        mock_slice_result = MagicMock()
        mock_slice_result.copy.return_value = final_mock_df

        # Mock the iloc __getitem__ to return the slice object
        mock_df.iloc.__getitem__.return_value = mock_slice_result

        trades_log = []

        # Test cases
        unsafe_filenames = [
            "../evil.png",
            "dir/evil.png",
            "/abs/evil.png",
            "win\\evil.png"
        ]

        for filename in unsafe_filenames:
            with self.subTest(filename=filename):
                # We expect ValueError. If it's not raised, the test fails.
                with self.assertRaises(ValueError, msg=f"Should have raised ValueError for {filename}"):
                    plot_results(mock_df, trades_log, filename=filename)

    @patch('bitcoin_sim.plt')
    def test_valid_filename(self, mock_plt):
        # Verification that valid filename works
        mock_df = MagicMock()
        final_mock_df = MagicMock()
        final_mock_df.__getitem__.return_value = [1, 2, 3]
        mock_slice_result = MagicMock()
        mock_slice_result.copy.return_value = final_mock_df
        mock_df.iloc.__getitem__.return_value = mock_slice_result

        trades_log = []

        try:
            plot_results(mock_df, trades_log, filename="safe.png")
        except ValueError:
            self.fail("plot_results raised ValueError on valid filename")

if __name__ == '__main__':
    unittest.main()
