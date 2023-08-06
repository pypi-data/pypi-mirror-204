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

from __future__ import annotations

import datetime

__all__ = [
    "Post",
]


class Post:
    """
    A class representing a cbmc post.
    """

    def __init__(self, data: dict) -> None:
        """
        Initialize the post.

        :param data: The data of the post.
        :type data: dict
        """
        self._post_id = data.get("id", {}).get("post")
        self._platform_id = data.get("id", {}).get("platform")
        self._type = data.get("type")
        self._content = data.get("content")
        self._photo = data.get("photo")
        self._admin_post = data.get("adminPost")
        self._approve_timestamp = data.get("approve", {}).get("timestamp")
        self._approve_user = data.get("approve", {}).get("user")
        self._fbid = data.get("fbid")

        if self._approve_timestamp is not None:
            approve_time = datetime.datetime.utcfromtimestamp(self._approve_timestamp)
            self._approve_time = approve_time.replace(tzinfo=datetime.timezone.utc)
        else:
            self._approve_time = None

    @property
    def post_id(self) -> int:
        """
        The post ID of the post.

        :return: The value of the post ID.
        :rtype: int
        """
        return self._post_id

    @property
    def platform_id(self) -> int:
        """
        The platform ID of the post.

        :return: The value of the platform ID.
        :rtype: int
        """
        return self._platform_id

    @property
    def type(self) -> str:
        """
        The post type of the post.

        :return: The value of the post type.
        :rtype: str
        """
        return self._type

    @property
    def content(self) -> str:
        """
        The content of the post.

        :return: The value of the content.
        :rtype: str
        """
        return self._content

    @property
    def photo(self) -> str | None:
        """
        The photo url of the post.

        :return: The post photo url or None if there is no photo.
        :rtype: str | None
        """
        return self._photo

    @property
    def admin_post(self) -> bool:
        """
        Whether the post is an admin post.

        :return: Whether the post is an admin post.
        :rtype: bool
        """
        return self._admin_post

    @property
    def approve_time(self) -> datetime.datetime:
        """
        The time the post was approved in UTC.

        :return: The time the post was approved.
        :rtype: datetime.datetime
        """
        return self._approve_time

    @property
    def approve_timestamp(self) -> int:
        """
        The Unix timestamp the post was approved in UTC.

        :return: The timestamp the post was approved.
        :rtype: int
        """
        return self._approve_timestamp

    @property
    def approve_user(self) -> str:
        """
        The user who approved the post.

        :return: The user who approved the post.
        :rtype: str
        """
        return self._approve_user

    @property
    def fbid(self) -> str:
        """
        The fbid of the post.

        :return: The post fbid.
        :rtype: str
        """
        return self._fbid

    def to_dict(self) -> dict:
        """
        Get the post as a dictionary.

        :return: The post as a dictionary.
        :rtype: dict
        """
        return {
            "post_id": self.post_id,
            "platform_id": self.platform_id,
            "type": self.type,
            "content": self.content,
            "photo": self.photo,
            "admin_post": self.admin_post,
            "approve_time": self.approve_time,
            "approve_timestamp": self.approve_timestamp,
            "approve_user": self.approve_user,
            "fbid": self.fbid,
        }

    def __repr__(self) -> str:
        """
        Get the string representation of the post.

        :return: The string representation of the post.
        :rtype: str
        """
        return f"<Post post_id={self.post_id} platform_id={self.platform_id}>"

    def __str__(self) -> str:
        """
        Get the string representation of the post.

        :return: The string representation of the post.
        :rtype: str
        """
        return self.content
