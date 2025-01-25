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

    def list_files(self):
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            return [obj['Key'] for obj in response.get('Contents', [])]
        except Exception:
            return []

class File:
    def __init__(self, file_key: str):
        self.file_key = file_key

    def is_txt_file(self) -> bool:
        return self.file_key.endswith('.txt')

    def print_contents(self, bucket_name: str):
        try:
            s3_client = boto3.client('s3')
            obj = s3_client.get_object(Bucket=bucket_name, Key=self.file_key)
            print(obj['Body'].read().decode('utf-8'))
        except Exception as e:
            print(f"Error reading file {self.file_key}: {e}")

if __name__ == "__main__":
    bucket_name = "api1-bucket"
    bucket = Bucket(bucket_name)

    if bucket.bucket_exists():
        print(f"Bucket '{bucket_name}' exists.")
        files = bucket.list_files()

        if files:
            print(f"Found files: {', '.join(files)}")
            for file_key in files:
                file = File(file_key)
                if file.is_txt_file():
                    print(f"\nContents of {file_key}:")
                    file.print_contents(bucket_name)
        else:
            print("The bucket is empty.")
    else:
        print(f"Bucket '{bucket_name}' does not exist.")
