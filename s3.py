import boto3

class Bucket:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    def bucket_exists(self) -> bool:
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except Exception:
            return False

    def print_txt_files(self):
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            files = [obj['Key'] for obj in response.get('Contents', [])]
            for file_key in files:
                if file_key.endswith('.txt'):
                    print(f"Contents of {file_key}:")
                    obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
                    print(obj['Body'].read().decode('utf-8'))
        except Exception as e:
            raise Exception(f"Error printing .txt files: {e}")


class File:
    def __init__(self, file_key: str):
        self.file_key = file_key

    def check_if_file_is_txt_file(self) -> bool:
        return self.file_key.endswith('.txt')

    def print_contents(self, bucket_name: str):
        try:
            s3_client = boto3.client('s3')
            obj = s3_client.get_object(Bucket=bucket_name, Key=self.file_key)
            print(obj['Body'].read().decode('utf-8'))
        except Exception as e:
            raise Exception(f"Error printing file contents: {e}")
