from __future__ import annotations

from typing import BinaryIO, Iterator
from urllib.parse import quote

import boto3
from botocore.client import BaseClient
from botocore.config import Config
from botocore.exceptions import ClientError
from django.conf import settings


class Bucket:
    """
    A secure S3-compatible object storage client for ArvanCloud.

    Supports uploading, reading, updating, deleting, listing objects,
    generating URLs, and checking object existence.
    """

    def __init__(self) -> None:
        """Initialize the S3 client using Django settings."""

        config = settings.ARVAN_S3_CONFIG

        self.bucket_name: str = config["bucket_name"]
        self.cdn_domain: str = config["cdn_domain"]

        self.client: BaseClient = boto3.client(
            "s3",
            endpoint_url=config["endpoint_url"],
            aws_access_key_id=config["access_key"],
            aws_secret_access_key=config["secret_key"],
            region_name="us-east-1",
            config=Config(
                signature_version="s3v4",
                s3={"addressing_style": "path"},
                connect_timeout=5,
                read_timeout=30,
                retries={
                    "max_attempts": 3,
                    "mode": "standard",
                },
            ),
        )

    @staticmethod
    def _validate_key(key: str) -> str:
        """
        Validate an object key to prevent unsafe paths.

        Args:
            key: The object key in the bucket.

        Returns:
            A normalized object key.

        Raises:
            ValueError: If the key is invalid.
        """

        if not isinstance(key, str) or not key.strip():
            raise ValueError("Object key cannot be empty.")

        key = key.strip()

        if key.startswith("/") or "\\" in key:
            raise ValueError("Invalid object key.")

        parts = key.split("/")

        if any(part in {"", ".", ".."} for part in parts):
            raise ValueError("Invalid object key path.")

        return key

    def upload(
        self,
        key: str,
        file: BinaryIO | bytes,
        content_type: str | None = None,
    ) -> str:
        """
        Upload a file to the bucket.

        If the object already exists, it will be overwritten.

        Args:
            key: Destination object key.
            file: Binary file object or bytes.
            content_type: Optional MIME type.

        Returns:
            The uploaded object's URL.
        """

        key = self._validate_key(key)

        extra_args: dict[str, str] = {}

        if content_type:
            extra_args["ContentType"] = content_type

        if isinstance(file, bytes):
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file,
                **extra_args,
            )
        else:
            self.client.upload_fileobj(
                Fileobj=file,
                Bucket=self.bucket_name,
                Key=key,
                ExtraArgs=extra_args or None,
            )

        return self.get_url(key)

    def read(self, key: str) -> bytes:
        """
        Read an object from the bucket.

        Args:
            key: Object key.

        Returns:
            File contents as bytes.
        """

        key = self._validate_key(key)

        response = self.client.get_object(
            Bucket=self.bucket_name,
            Key=key,
        )

        body = response["Body"]

        try:
            return body.read()
        finally:
            body.close()

    def get_url(
        self,
        key: str,
        expires_in: int = 3600,
    ) -> str:
        """
        Generate a URL for an object.

        Public objects use the CDN domain.
        Without a CDN domain, a temporary presigned URL is returned.

        Args:
            key: Object key.
            expires_in: Presigned URL expiration in seconds.

        Returns:
            Public CDN URL or a temporary presigned URL.
        """

        key = self._validate_key(key)

        if self.cdn_domain:
            encoded_key = quote(key, safe="/")
            return f"{self.cdn_domain}/{encoded_key}"

        if not 1 <= expires_in <= 604800:
            raise ValueError("Expiration must be between 1 and 604800 seconds.")

        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": key,
            },
            ExpiresIn=expires_in,
        )

    def update(
        self,
        key: str,
        file: BinaryIO | bytes,
        content_type: str | None = None,
    ) -> str:
        """
        Replace an existing object's contents.

        Args:
            key: Existing object key.
            file: New file contents.
            content_type: Optional MIME type.

        Returns:
            Updated object's URL.

        Raises:
            FileNotFoundError: If the object does not exist.
        """

        key = self._validate_key(key)

        if not self.exists(key):
            raise FileNotFoundError(f"Object '{key}' does not exist.")

        return self.upload(
            key=key,
            file=file,
            content_type=content_type,
        )

    def delete(self, key: str) -> None:
        """
        Delete an object from the bucket.

        Args:
            key: Object key.
        """

        key = self._validate_key(key)

        self.client.delete_object(
            Bucket=self.bucket_name,
            Key=key,
        )

    def exists(self, key: str) -> bool:
        """
        Check whether an object exists in the bucket.

        Args:
            key: Object key.

        Returns:
            True if the object exists, otherwise False.
        """

        key = self._validate_key(key)

        try:
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=key,
            )
            return True

        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code", "")

            if error_code in {"404", "NoSuchKey", "NotFound"}:
                return False

            raise

    def list_files(
        self,
        prefix: str = "",
    ) -> Iterator[dict[str, object]]:
        """
        List objects under a prefix.

        Uses pagination to handle large buckets.

        Args:
            prefix: Optional key prefix.

        Yields:
            Object metadata dictionaries.
        """

        if prefix.startswith("/") or "\\" in prefix:
            raise ValueError("Invalid prefix.")

        paginator = self.client.get_paginator("list_objects_v2")

        pages = paginator.paginate(
            Bucket=self.bucket_name,
            Prefix=prefix,
        )

        for page in pages:
            for item in page.get("Contents", []):
                yield {
                    "key": item["Key"],
                    "size": item["Size"],
                    "last_modified": item["LastModified"],
                    "etag": item["ETag"],
                }

    def get_metadata(self, key: str) -> dict[str, object]:
        """
        Retrieve object metadata without downloading its contents.

        Args:
            key: Object key.

        Returns:
            Object metadata.
        """

        key = self._validate_key(key)

        response = self.client.head_object(
            Bucket=self.bucket_name,
            Key=key,
        )

        return {
            "content_type": response.get("ContentType"),
            "content_length": response.get("ContentLength"),
            "last_modified": response.get("LastModified"),
            "etag": response.get("ETag"),
            "metadata": response.get("Metadata", {}),
        }