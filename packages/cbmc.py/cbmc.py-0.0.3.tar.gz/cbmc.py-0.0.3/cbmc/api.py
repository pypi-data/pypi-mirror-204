"""
MIT License

Copyright (c) 2023 ItsRqtl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import List

import aiohttp
import requests

from .exception import HTTPException, NotFound
from .post import Post

__all__ = [
    "AsyncCbmc",
    "SyncCbmc",
]


class CbmcBase:
    """
    The base class for the CBMC API.
    """

    base_url = "https://api.cbmc.club/v1"


class SyncCbmc(CbmcBase):
    """
    A synchronous wrapper for the CBMC API.
    """

    @classmethod
    def get_post(cls, post_id: int) -> Post:
        """
        Get a post by its ID.

        :param post_id: The ID of the post.
        :type post_id: int

        :raise TypeError: The post ID is not an integer.
        :raise NotFound: The post was not found.
        :raise HTTPException: The HTTP request failed.

        :return: The post object.
        :rtype: Post
        """
        if not isinstance(post_id, int):
            raise TypeError("The post ID must be an integer.")
        url = f"{cls.base_url}/post/{post_id}"
        with requests.get(url) as resp:
            if resp.status_code == 200:
                data = resp.json()
                if data["status"] == "failed":
                    raise NotFound(data.get("message", "Post not found."))
                elif data["status"] == "success" and "posts" in data:
                    return Post(data["posts"]["1"]["post"])
            raise HTTPException(f"HTTP request failed with status code {resp.status_code}.")

    @classmethod
    def get_posts(cls, limit: int = 10) -> List[Post]:
        """
        Get the latest posts.

        :param limit: The maximum number of posts to return.
        :type limit: int

        :raise TypeError: The limit is not an integer.
        :raise ValueError: The limit is greater than 300 or less than 1.
        :raise HTTPException: The HTTP request failed.

        :return: A list of post objects.
        :rtype: List[Post]
        """
        if not isinstance(limit, int):
            raise TypeError("The limit must be an integer.")
        if limit > 300 or limit < 1:
            raise ValueError("The maximum number of posts to return must be between 1 and 300.")
        url = f"{cls.base_url}/latest?limit={limit}"
        with requests.get(url) as resp:
            if resp.status_code == 200:
                data = resp.json()
                if data["status"] == "success" and "posts" in data:
                    return [Post(i["post"]) for i in data["posts"].values()]
            raise HTTPException(f"HTTP request failed with status code {resp.status_code}.")

    @classmethod
    def get_status(cls, code: str) -> dict:
        """
        Get a status by its code.

        :param code: The query code of the status.
        :type code: str

        :return: The status.
        :rtype: dict
        """
        raise NotImplementedError


class AsyncCbmc(CbmcBase):
    """
    An asynchronous wrapper for the CBMC API.
    """

    @classmethod
    async def get_post(cls, post_id: int) -> Post:
        """
        Get a post by its ID.

        :param post_id: The ID of the post.
        :type post_id: int

        :raise TypeError: The post ID is not an integer.
        :raise NotFound: The post was not found.
        :raise HTTPException: The HTTP request failed.

        :return: The post object.
        :rtype: Post
        """
        if not isinstance(post_id, int):
            raise TypeError("The post ID must be an integer.")
        url = f"{cls.base_url}/post/{post_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data["status"] == "failed":
                        raise NotFound(data.get("message", "Post not found."))
                    elif data["status"] == "success" and "posts" in data:
                        return Post(data["posts"]["1"]["post"])
                raise HTTPException(f"HTTP request failed with status code {resp.status}.")

    @classmethod
    async def get_posts(cls, limit: int = 10) -> List[Post]:
        """
        Get the latest posts.

        :param limit: The maximum number of posts to return.
        :type limit: int

        :raise TypeError: The limit is not an integer.
        :raise ValueError: The limit is greater than 300 or less than 1.
        :raise HTTPException: The HTTP request failed.

        :return: A list of post objects.
        :rtype: List[Post]
        """
        if not isinstance(limit, int):
            raise TypeError("The limit must be an integer.")
        if limit > 300 or limit < 1:
            raise ValueError("The maximum number of posts to return must be between 1 and 300.")
        url = f"{cls.base_url}/latest?limit={limit}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data["status"] == "success" and "posts" in data:
                        return [Post(i["post"]) for i in data["posts"].values()]
                raise HTTPException(f"HTTP request failed with status code {resp.status}.")

    @classmethod
    async def get_status(cls, code: str) -> dict:
        """
        Get a status by its code.

        :param code: The query code of the status.
        :type code: str

        :return: The status.
        :rtype: dict
        """
        raise NotImplementedError
