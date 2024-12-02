import os

class S3Manager:
    def __init__(self, local_path):
        self.local_path = local_path

    def check_bucket(self, bucket_name):
        bucket_path = os.path.join(self.local_path, bucket_name)
        
        # Check if bucket exists
        if not os.path.exists(bucket_path):
            return f"Bucket '{bucket_name}' does not exist."
        
        # Check if bucket is empty
        objects = os.listdir(bucket_path)
        if not objects:
            return f"Bucket '{bucket_name}' is empty."

        # Check for .txt files
        txt_files = [file for file in objects if file.endswith('.txt')]
        if not txt_files:
            return (
                f"Bucket '{bucket_name}' contains {len(objects)} files, "
                "but no .txt files."
            )

        return (
            f"Bucket '{bucket_name}' contains {len(objects)} files, "
            f"including {len(txt_files)} .txt files."
        )

if __name__ == "__main__":
    # Use the local directory as a simulation of S3
    local_path = r"C:\Users\karth\OneDrive\Desktop\Unit-testing"
    manager = S3Manager(local_path=local_path)

    # Get bucket name from the user
    bucket_name = input("Enter the bucket name to check: ").strip()
    if not bucket_name:
        print("Bucket name cannot be empty.")
    else:
        result = manager.check_bucket(bucket_name)
        print(result)
