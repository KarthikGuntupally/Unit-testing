from unittest.mock import patch
from main import S3Manager

# Test 1: Bucket does not exist
def test_bucket_does_not_exist():
    with patch("os.path.exists", return_value=False):
        manager = S3Manager(local_path="/mock/bucket")
        result = manager.check_bucket("nonexistent-bucket")
        assert result == "Bucket 'nonexistent-bucket' does not exist."

# Test 2: Bucket is empty
def test_empty_bucket():
    with patch("os.path.exists", return_value=True), \
         patch("os.listdir", return_value=[]):
        manager = S3Manager(local_path="/mock/bucket")
        result = manager.check_bucket("bucket1")
        assert result == "Bucket 'bucket1' is empty."

# Test 3: Bucket with objects but no .txt files
def test_bucket_with_no_txt_files():
    with patch("os.path.exists", return_value=True), \
         patch("os.listdir", return_value=["file1.jpg", "file2.png"]):
        manager = S3Manager(local_path="/mock/bucket")
        result = manager.check_bucket("bucket2")
        assert result == "Bucket 'bucket2' contains 2 files, but no .txt files."

# Test 4: Bucket with objects including .txt files
def test_bucket_with_txt_files():
    with patch("os.path.exists", return_value=True), \
         patch("os.listdir", return_value=["file1.txt", "file2.jpg"]):
        manager = S3Manager(local_path="/mock/bucket")
        result = manager.check_bucket("bucket3")
        assert result == "Bucket 'bucket3' contains 2 files, including 1 .txt files."

# Test 5: Bucket with only .txt files
def test_bucket_with_only_txt_files():
    with patch("os.path.exists", return_value=True), \
         patch("os.listdir", return_value=["file1.txt", "file2.txt"]):
        manager = S3Manager(local_path="/mock/bucket")
        result = manager.check_bucket("bucket4")
        assert result == "Bucket 'bucket4' contains 2 files, including 2 .txt files."
