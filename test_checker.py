import unittest
import os
import shutil
import json
from pathlib import Path
from Checker import hash_file, get_dir_hashes, check_integrity, save_hashes, load_hashes

class TestChecker(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_sandbox")
        self.test_dir.mkdir(exist_ok=True)
        self.file1 = self.test_dir / "file1.txt"
        self.file1.write_text("hello world")
        self.file2 = self.test_dir / "file2.txt"
        self.file2.write_text("integrity test")
        self.json_path = Path("test_hashes.json")

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        if self.json_path.exists():
            self.json_path.unlink()

    def test_hash_file(self):
        h1 = hash_file(self.file1)
        h2 = hash_file(self.file1)
        self.assertEqual(h1, h2)
        
        # SHA-256 for "hello world"
        import hashlib
        expected = hashlib.sha256(b"hello world").hexdigest()
        self.assertEqual(h1, expected)

    def test_get_dir_hashes(self):
        hashes = get_dir_hashes(self.test_dir)
        self.assertIn("file1.txt", hashes)
        self.assertIn("file2.txt", hashes)
        self.assertEqual(len(hashes), 2)

    def test_check_integrity_intact(self):
        baseline = get_dir_hashes(self.test_dir)
        results = check_integrity(self.test_dir, baseline)
        self.assertFalse(results["missing"])
        self.assertFalse(results["added"])
        self.assertFalse(results["tampered"])

    def test_check_integrity_tampered(self):
        baseline = get_dir_hashes(self.test_dir)
        self.file1.write_text("hello tampered world")
        results = check_integrity(self.test_dir, baseline)
        self.assertIn("file1.txt", results["tampered"])
        self.assertFalse(results["missing"])
        self.assertFalse(results["added"])

    def test_check_integrity_missing(self):
        baseline = get_dir_hashes(self.test_dir)
        self.file2.unlink()
        results = check_integrity(self.test_dir, baseline)
        self.assertIn("file2.txt", results["missing"])
        self.assertFalse(results["added"])
        self.assertFalse(results["tampered"])

    def test_check_integrity_added(self):
        baseline = get_dir_hashes(self.test_dir)
        file3 = self.test_dir / "file3.txt"
        file3.write_text("new file")
        results = check_integrity(self.test_dir, baseline)
        self.assertIn("file3.txt", results["added"])
        self.assertFalse(results["missing"])
        self.assertFalse(results["tampered"])

    def test_save_load_hashes(self):
        hashes = {"test.txt": "12345"}
        save_hashes(hashes, self.json_path)
        loaded = load_hashes(self.json_path)
        self.assertEqual(hashes, loaded)

if __name__ == "__main__":
    unittest.main()
