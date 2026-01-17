import unittest
import os
import sys
import tempfile
import shutil

# Configure matplotlib backend BEFORE importing modules that use pyplot
import matplotlib
matplotlib.use('Agg')

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results, SimConfig, generate_synthetic_data, calculate_indicators

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Setup dummy data
        self.config = SimConfig(days=100)
        self.df = generate_synthetic_data(self.config)
        self.df = calculate_indicators(self.df)
        self.df = self.df.dropna().reset_index(drop=True)
        self.trades = []

    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_path_traversal_plot_results(self):
        # Attempt to write to parent directory
        # The fix should now raise a ValueError

        target_file = "attack_plot.png"
        traversal_path = os.path.join("..", target_file)

        with self.assertRaises(ValueError) as cm:
            plot_results(self.df, self.trades, filename=traversal_path)

        self.assertIn("Security Error", str(cm.exception))
        self.assertIn("contains path components", str(cm.exception))

        # Also test absolute path (should also fail as it contains directory components)
        abs_path = os.path.join(self.test_dir, "subdir", "test.png")
        with self.assertRaises(ValueError) as cm:
            plot_results(self.df, self.trades, filename=abs_path)

    def test_valid_filename(self):
        # Should succeed
        plot_results(self.df, self.trades, filename="valid_plot.png")
        self.assertTrue(os.path.exists("valid_plot.png"))

if __name__ == "__main__":
    unittest.main()
