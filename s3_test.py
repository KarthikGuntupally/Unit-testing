import unittest
from unittest.mock import patch, MagicMock
from s3 import Bucket, File


class TestBucket(unittest.TestCase):
    @patch('boto3.client')
    def test_bucket_not_exists(self, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.head_bucket.side_effect = Exception("Bucket does not exist")

        bucket = Bucket(bucket_name="non-existing-bucket")
        self.assertFalse(bucket.bucket_exists())
    
    @patch('boto3.client')
    def test_bucket_exists(self, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.head_bucket.return_value = {}

        bucket = Bucket(bucket_name="existing-bucket")
        self.assertTrue(bucket.bucket_exists())

    @patch('boto3.client')
    @patch('builtins.print')
    def test_bucket_with_txt_files(self, mock_print, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.list_objects_v2.return_value = {
            'Contents': [
                {'Key': 'file1.txt'},
                {'Key': 'file2.jpg'},
                {'Key': 'file3.txt'}
            ]
        }
        bucket = Bucket(bucket_name="test-bucket")
        files = bucket.list_files()

        self.assertIn('file1.txt', files)
        self.assertIn('file3.txt', files)
        self.assertIn('file2.jpg', files)

    @patch('boto3.client')
    def test_bucket_with_non_txt_files_only(self, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.list_objects_v2.return_value = {
            'Contents': [
                {'Key': 'file1.jpg'},
                {'Key': 'file2.png'}
            ]
        }
        bucket = Bucket(bucket_name="test-bucket")
        files = bucket.list_files()

        self.assertNotIn('file1.txt', files)
        self.assertNotIn('file2.txt', files)

    @patch('boto3.client')
    def test_bucket_empty(self, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.list_objects_v2.return_value = {}

        bucket = Bucket(bucket_name="empty-bucket")
        files = bucket.list_files()
        self.assertEqual(len(files), 0)


class TestFile(unittest.TestCase):
    def test_file_is_txt(self):
        file = File(file_key="example.txt")
        self.assertTrue(file.is_txt_file())

    def test_file_is_not_txt(self):
        file = File(file_key="example.jpg")
        self.assertFalse(file.is_txt_file())

if __name__ == "__main__":
    unittest.main()
