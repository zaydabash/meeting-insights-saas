import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from typing import BinaryIO, Optional
from app.core.config import settings
import uuid


class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            config=Config(signature_version="s3v4"),
            region_name=settings.s3_region,
        )
        self._ensure_buckets()

    def _ensure_buckets(self):
        buckets = [settings.s3_bucket_audio, settings.s3_bucket_transcripts]
        for bucket in buckets:
            try:
                self.s3_client.head_bucket(Bucket=bucket)
            except ClientError:
                self.s3_client.create_bucket(Bucket=bucket)

    def upload_audio(self, file: BinaryIO, filename: Optional[str] = None) -> str:
        key = f"audio/{uuid.uuid4()}/{filename or 'audio.mp3'}"
        self.s3_client.upload_fileobj(file, settings.s3_bucket_audio, key)
        return key

    def upload_transcript(self, content: str, meeting_id: int) -> str:
        key = f"transcripts/{meeting_id}/transcript.txt"
        self.s3_client.put_object(
            Bucket=settings.s3_bucket_transcripts,
            Key=key,
            Body=content.encode("utf-8"),
        )
        return key

    def get_signed_url(self, bucket: str, key: str, expiration: int = 3600) -> str:
        return self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expiration,
        )

    def get_audio_url(self, key: str) -> str:
        return self.get_signed_url(settings.s3_bucket_audio, key)


storage_service = StorageService()

