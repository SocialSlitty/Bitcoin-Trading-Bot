import unittest
import os
import shutil
import tempfile
import pandas as pd
import matplotlib
# Use Agg backend for non-interactive environments
matplotlib.use('Agg')
from src.bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create a dummy dataframe and trades log
        self.df = pd.DataFrame({
            "Date": pd.date_range(start="2023-01-01", periods=100),
            "Close": [100.0] * 100,
            "EMA_7": [100.0] * 100,
            "SMA_30": [100.0] * 100,
            "SMA_200": [100.0] * 100,
            "Open": [100.0] * 100,
            "High": [100.0] * 100,
            "Low": [100.0] * 100,
            "Volume": [1000] * 100
        })
        self.trades_log = []
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_valid_filename(self):
        """Test that a valid filename works correctly."""
        filename = "test_plot.png"
        try:
            plot_results(self.df, self.trades_log, filename=filename)
            self.assertTrue(os.path.exists(filename))
        except ValueError:
            self.fail("plot_results raised ValueError unexpectedly!")

    def test_path_traversal_absolute(self):
        """Test that an absolute path raises ValueError."""
        # /tmp/foo.png
        filename = os.path.join(self.test_dir, "absolute_path.png")
        with self.assertRaises(ValueError) as cm:
            plot_results(self.df, self.trades_log, filename=filename)
        self.assertIn("must not contain path components", str(cm.exception))

    def test_path_traversal_relative(self):
        """Test that a relative path with directory components raises ValueError."""
        # ./foo.png or ../foo.png
        filename = os.path.join("subdir", "relative_path.png")
        with self.assertRaises(ValueError) as cm:
            plot_results(self.df, self.trades_log, filename=filename)
        self.assertIn("must not contain path components", str(cm.exception))

        filename = "../parent_path.png"
        with self.assertRaises(ValueError) as cm:
            plot_results(self.df, self.trades_log, filename=filename)
        self.assertIn("must not contain path components", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
