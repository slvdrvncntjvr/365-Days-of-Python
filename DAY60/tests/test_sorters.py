"""
Tests for the sorters module.
"""

import os
import shutil
import tempfile
import unittest
from organizer.sorters import organize_by_extension, organize_by_date, organize_by_size

class TestSorters(unittest.TestCase):
    """Test cases for file sorting functions."""
    
    def setUp(self):
        """Set up a temporary directory for testing."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create some test files
        with open(os.path.join(self.temp_dir, "test.txt"), "w") as f:
            f.write("test content")
        
        with open(os.path.join(self.temp_dir, "example.py"), "w") as f:
            f.write("print('Hello, world!')")
        
        with open(os.path.join(self.temp_dir, "data.csv"), "w") as f:
            f.write("name,age\nAlice,30\nBob,25")
    
    def tearDown(self):
        """Clean up the temporary directory."""
        shutil.rmtree(self.temp_dir)
    
    def test_organize_by_extension(self):
        """Test organizing files by extension."""
        result = organize_by_extension(self.temp_dir)
        
        # Check that the directories were created
        self.assertTrue(os.path.isdir(os.path.join(self.temp_dir, "txt")))
        self.assertTrue(os.path.isdir(os.path.join(self.temp_dir, "py")))
        self.assertTrue(os.path.isdir(os.path.join(self.temp_dir, "csv")))
        
        # Check that the files were moved
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "txt", "test.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "py", "example.py")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "csv", "data.csv")))
        
        # Check the returned dictionary
        self.assertEqual(set(result.keys()), {"txt", "py", "csv"})
        self.assertEqual(result["txt"], ["test.txt"])
        self.assertEqual(result["py"], ["example.py"])
        self.assertEqual(result["csv"], ["data.csv"])

if __name__ == "__main__":
    unittest.main()