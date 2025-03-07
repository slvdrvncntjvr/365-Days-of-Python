"""
Tests for the utils module.
"""

import os
import tempfile
import unittest
from organizer.utils import count_files_in_dir, get_file_size_category

class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_count_files_in_dir(self):
        """Test counting files in a directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some test files
            with open(os.path.join(temp_dir, "file1.txt"), "w") as f:
                f.write("test content")
            
            with open(os.path.join(temp_dir, "file2.txt"), "w") as f:
                f.write("more content")
            
            # Create a subdirectory (should not be counted)
            os.makedirs(os.path.join(temp_dir, "subdir"))
            
            # Count files
            count = count_files_in_dir(temp_dir)
            self.assertEqual(count, 2)
    
    def test_get_file_size_category(self):
        """Test file size categorization."""
        # Test various file sizes
        self.assertEqual(get_file_size_category(500), "tiny_less_than_1KB")
        self.assertEqual(get_file_size_category(5 * 1024), "small_1KB_10KB")
        self.assertEqual(get_file_size_category(50 * 1024), "medium_10KB_100KB")
        self.assertEqual(get_file_size_category(500 * 1024), "large_100KB_1MB")
        self.assertEqual(get_file_size_category(5 * 1024 * 1024), "very_large_1MB_10MB")
        self.assertEqual(get_file_size_category(50 * 1024 * 1024), "huge_10MB_100MB")
        self.assertEqual(get_file_size_category(500 * 1024 * 1024), "enormous_100MB_1GB")
        self.assertEqual(get_file_size_category(5 * 1024 * 1024 * 1024), "massive_over_1GB")

if __name__ == "__main__":
    unittest.main()