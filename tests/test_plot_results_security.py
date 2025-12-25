import unittest
import sys
import os
import tempfile
import shutil

# Add src to path to allow importing bitcoin_sim
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from bitcoin_sim import plot_results, generate_synthetic_data, calculate_indicators, SimConfig


class TestPlotResultsSecurity(unittest.TestCase):
    """Test path traversal security in plot_results function."""

    def setUp(self):
        """Set up test data."""
        # Generate minimal test data
        config = SimConfig(days=70)  # Enough for indicators + 60 days simulation
        df = generate_synthetic_data(config)
        df = calculate_indicators(df)
        df = df.dropna().reset_index(drop=True)
        self.df = df
        self.trades_log = []

    def test_safe_filename_current_dir(self):
        """Test that a simple filename in current directory is allowed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            filename = "test_safe.png"
            try:
                plot_results(self.df, self.trades_log, filename=filename)
                self.assertTrue(os.path.exists(filename))
            finally:
                if os.path.exists(filename):
                    os.remove(filename)

    def test_safe_filename_subdirectory(self):
        """Test that a filename in a subdirectory is allowed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            os.makedirs("subdir", exist_ok=True)
            filename = "subdir/test_safe.png"
            try:
                plot_results(self.df, self.trades_log, filename=filename)
                self.assertTrue(os.path.exists(filename))
            finally:
                if os.path.exists(filename):
                    os.remove(filename)

    def test_unsafe_filename_parent_dir(self):
        """Test that path traversal to parent directory is blocked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            filename = "../test_unsafe.png"
            with self.assertRaisesRegex(ValueError, "Security Error"):
                plot_results(self.df, self.trades_log, filename=filename)
            # Verify file was NOT created in parent directory
            parent_file = os.path.join(os.path.dirname(tmpdir), "test_unsafe.png")
            self.assertFalse(os.path.exists(parent_file))

    def test_unsafe_filename_absolute_path(self):
        """Test that absolute paths outside CWD are blocked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            filename = "/tmp/test_unsafe.png"
            with self.assertRaisesRegex(ValueError, "Security Error"):
                plot_results(self.df, self.trades_log, filename=filename)
            self.assertFalse(os.path.exists(filename))

    def test_unsafe_filename_multiple_traversal(self):
        """Test that multiple directory traversals are blocked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            filename = "../../etc/passwd"
            with self.assertRaisesRegex(ValueError, "Security Error"):
                plot_results(self.df, self.trades_log, filename=filename)


if __name__ == "__main__":
    unittest.main()
