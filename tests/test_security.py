import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from bitcoin_sim import SimConfig, plot_results

class TestSecurity(unittest.TestCase):

    def test_sim_config_dos_protection(self):
        """Test that SimConfig limits the maximum number of days to prevent DoS."""
        # This should fail initially as there is no upper limit
        with self.assertRaises(ValueError, msg="Should raise ValueError for excessive days"):
            SimConfig(days=1_000_000)

        # Boundary check (36500 is allowed, 36501 is not)
        try:
            SimConfig(days=36500)
        except ValueError:
            self.fail("SimConfig raised ValueError for valid max days (36500)")

        with self.assertRaises(ValueError):
            SimConfig(days=36501)

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
    @patch('matplotlib.pyplot.gca')
    def test_plot_results_path_traversal(self, mock_gca, *args):
        """Test that plot_results rejects filenames with path components."""

        # Setup mock DF
        df_mock = MagicMock()
        # Mocking iloc[-60:].copy()
        df_mock.iloc.__getitem__.return_value.copy.return_value = df_mock
        # Mock column access to return iterable/plottable mocks
        df_mock.__getitem__.return_value = MagicMock()

        trades_log = []

        # Mock gca return
        mock_ax = MagicMock()
        mock_ax.get_legend_handles_labels.return_value = ([], [])
        mock_gca.return_value = mock_ax

        # 1. Test directory traversal
        with self.assertRaises(ValueError, msg="Should reject path traversal '../file.png'"):
            plot_results(df_mock, trades_log, filename="../evil.png")

        # 2. Test absolute path (Unix)
        with self.assertRaises(ValueError, msg="Should reject absolute path '/tmp/evil.png'"):
            plot_results(df_mock, trades_log, filename="/tmp/evil.png")

        # 3. Test simple valid filename
        try:
            plot_results(df_mock, trades_log, filename="safe_plot.png")
        except ValueError:
            self.fail("plot_results raised ValueError for valid filename")

if __name__ == '__main__':
    unittest.main()
