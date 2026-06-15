import boto3
from botocore.exceptions import ClientError
from app.core.config import settings

s3_client = boto3.client(
    "s3",
    region_name=settings.aws_region,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key
)

def upload_file(file_obj, folder: str, filename: str) -> str:
    key = f"{folder}/{filename}"
    try:
        s3_client.upload_fileobj(
            file_obj,
            settings.aws_bucket_name,
            key,
            ExtraArgs={"ACL": "private"}
        )
        return key
    except ClientError as e:
        print(f"S3 upload error: {e}")
        raise


def generate_presigned_url(key: str, expiry: int = 3600) -> str:
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.aws_bucket_name, "Key": key},
            ExpiresIn=expiry
        )
        return url
    except ClientError as e:
        print(f"S3 presigned URL error: {e}")
        raise
    
    
    
def delete_file(key: str) -> bool:
    try:
        s3_client.delete_object(
            Bucket=settings.aws_bucket_name,
            Key=key,
        )
        return True
    except ClientError as e:
        print(f"S3 delete error: {e}")
        return False