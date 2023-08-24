import asyncio
import os
from typing import List

import aiohttp
import boto3


class UploadVideosToS3:
    def __init__(self, aws_access_key_id: str = os.environ.get("AWS_ACCESS_KEY_ID"),
                 aws_secret_access_key: str = os.environ.get("AWS_SECRET_ACCESS_KEY"),
                 bucket_name: str = os.environ.get("BUCKET_NAME")):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.bucket_name = bucket_name

    async def upload_video_to_s3(self, filename: str, url: str, username: str) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                with open(filename, "wb") as f:
                    async for data in response.content.iter_chunked(1024):
                        f.write(data)

        s3 = boto3.client("s3",
                          aws_access_key_id=self.aws_access_key_id,
                          aws_secret_access_key=self.aws_secret_access_key)
        with open(filename, "rb") as f:
            key = "{}/{}".format(username, filename)
            s3.upload_fileobj(f, self.bucket_name, key)
        os.remove(filename)

    async def upload_videos_to_s3(self, videos: List[dict]) -> None:
        """
        :param videos:
        videos = [
                {"filename": "video1.mp4", "url": "https://example.com/video1.mp4", "category": "category1"},
                {"filename": "video2.mp4", "url": "https://example.com/video2.mp4", "category": "category2"},
                {"filename": "video3.mp4", "url": "https://example.com/video3.mp4", "category": "category3"},
        ]
        :return:
        """
        tasks = []
        for video in videos:
            tasks.append(
                self.upload_video_to_s3(filename=video["filename"], url=video["url"], username=video["username"])
            )
        await asyncio.gather(*tasks)
