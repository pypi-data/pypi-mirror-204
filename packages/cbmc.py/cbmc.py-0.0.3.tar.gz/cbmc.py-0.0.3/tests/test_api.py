# sourcery skip: avoid-global-variables
import datetime

import requests_mock
from aioresponses import aioresponses
from pytest import raises

from cbmc.api import AsyncCbmc, SyncCbmc
from cbmc.exception import HTTPException, NotFound

pytest_plugins = ("pytest_asyncio",)


def test_sync_get_post() -> None:
    client = SyncCbmc()

    with requests_mock.Mocker() as m:
        m.get(
            f"{client.base_url}/post/1",
            json={
                "status": "success",
                "posts": {
                    "1": {
                        "post": {
                            "id": {"post": 1, "platform": 1},
                            "type": "靠北麥塊",
                            "content": "這是一篇靠北麥塊新站測試的第一篇文章\r\nhttps://cbmc.club/",
                            "photo": None,
                            "adminPost": True,
                            "approve": {
                                "time": "2021/11/12 19:17",
                                "timestamp": 1636715868,
                                "user": "單利",
                            },
                            "fbid": "924284348202766",
                        }
                    }
                },
            },
        )

        post = client.get_post(1)

        assert post.post_id == 1
        assert post.platform_id == 1
        assert post.type == "靠北麥塊"
        assert post.content == "這是一篇靠北麥塊新站測試的第一篇文章\r\nhttps://cbmc.club/"
        assert post.__str__() == "這是一篇靠北麥塊新站測試的第一篇文章\r\nhttps://cbmc.club/"
        assert post.photo is None
        assert post.admin_post is True
        assert post.approve_timestamp == 1636715868
        assert post.approve_time == datetime.datetime(
            2021, 11, 12, 11, 17, 48, tzinfo=datetime.timezone.utc
        )
        assert post.approve_user == "單利"
        assert post.fbid == "924284348202766"
        assert post.__repr__() == "<Post post_id=1 platform_id=1>"
        assert post.to_dict() == {
            "post_id": 1,
            "platform_id": 1,
            "type": "靠北麥塊",
            "content": "這是一篇靠北麥塊新站測試的第一篇文章\r\nhttps://cbmc.club/",
            "photo": None,
            "admin_post": True,
            "approve_time": datetime.datetime(
                2021, 11, 12, 11, 17, 48, tzinfo=datetime.timezone.utc
            ),
            "approve_timestamp": 1636715868,
            "approve_user": "單利",
            "fbid": "924284348202766",
        }


def test_sync_get_post_not_found() -> None:
    client = SyncCbmc()

    with requests_mock.Mocker() as m:
        m.get(
            f"{client.base_url}/post/1",
            json={"status": "failed", "message": "文章不存在、尚未經過審核或是被拒絕。"},
        )

        with raises(NotFound):
            client.get_post(1)


def test_sync_get_post_http_exception() -> None:
    client = SyncCbmc()

    with requests_mock.Mocker() as m:
        m.get(f"{client.base_url}/post/1", status_code=500)

        with raises(HTTPException):
            client.get_post(1)


def test_sync_get_post_type_error() -> None:
    client = SyncCbmc()

    with raises(TypeError):
        client.get_post("1")


def test_sync_get_posts() -> None:
    client = SyncCbmc()

    with requests_mock.Mocker() as m:
        m.get(
            f"{client.base_url}/latest?limit=2",
            json={
                "status": "success",
                "limit": 2,
                "posts": {
                    "1": {
                        "post": {
                            "id": {"post": 1703, "platform": 2067},
                            "type": "靠北麥塊",
                            "content": "確定某瑞只有跑去開GTA嗎?\r\n\r\n搞不好換了個名字 繼續開騙錢服 準備再次惡意倒閉呢\r\n\r\n呵呵呵~~",
                            "photo": None,
                            "adminPost": False,
                            "approve": {
                                "time": "2023/04/24 14:20",
                                "timestamp": 1682317224,
                                "user": "凱能",
                            },
                            "fbid": "557710793137813",
                        }
                    },
                    "2": {
                        "post": {
                            "id": {"post": 1701, "platform": 2065},
                            "type": "靠北麥塊",
                            "content": "某瑞惡意倒閉莊x後，就跑去開GTA夜xx城，賺的幾百萬",
                            "photo": None,
                            "adminPost": False,
                            "approve": {
                                "time": "2023/04/18 19:32",
                                "timestamp": 1681817560,
                                "user": "奧莉安娜",
                            },
                            "fbid": "554633576778868",
                        }
                    },
                },
            },
        )

        posts = client.get_posts(2)

        assert len(posts) == 2
        assert posts[0].post_id == 1703
        assert posts[0].platform_id == 2067
        assert posts[0].type == "靠北麥塊"
        assert posts[0].content == "確定某瑞只有跑去開GTA嗎?\r\n\r\n搞不好換了個名字 繼續開騙錢服 準備再次惡意倒閉呢\r\n\r\n呵呵呵~~"
        assert posts[0].__str__() == "確定某瑞只有跑去開GTA嗎?\r\n\r\n搞不好換了個名字 繼續開騙錢服 準備再次惡意倒閉呢\r\n\r\n呵呵呵~~"
        assert posts[0].photo is None
        assert posts[0].admin_post is False
        assert posts[0].approve_timestamp == 1682317224
        assert posts[0].approve_time == datetime.datetime(
            2023, 4, 24, 6, 20, 24, tzinfo=datetime.timezone.utc
        )
        assert posts[0].approve_user == "凱能"
        assert posts[0].fbid == "557710793137813"
        assert posts[0].__repr__() == "<Post post_id=1703 platform_id=2067>"
        assert posts[0].to_dict() == {
            "post_id": 1703,
            "platform_id": 2067,
            "type": "靠北麥塊",
            "content": "確定某瑞只有跑去開GTA嗎?\r\n\r\n搞不好換了個名字 繼續開騙錢服 準備再次惡意倒閉呢\r\n\r\n呵呵呵~~",
            "photo": None,
            "admin_post": False,
            "approve_time": datetime.datetime(2023, 4, 24, 6, 20, 24, tzinfo=datetime.timezone.utc),
            "approve_timestamp": 1682317224,
            "approve_user": "凱能",
            "fbid": "557710793137813",
        }


def test_sync_get_posts_http_exception() -> None:
    client = SyncCbmc()

    with requests_mock.Mocker() as m:
        m.get(f"{client.base_url}/latest?limit=2", status_code=500)

        with raises(HTTPException):
            client.get_posts(2)


def test_sync_get_posts_type_error() -> None:
    client = SyncCbmc()

    with raises(TypeError):
        client.get_posts("2")


def test_sync_get_posts_value_error() -> None:
    client = SyncCbmc()

    with raises(ValueError):
        client.get_posts(0)

    with raises(ValueError):
        client.get_posts(-1)

    with raises(ValueError):
        client.get_posts(301)


def test_sync_get_status() -> None:
    client = SyncCbmc()

    with raises(NotImplementedError):
        client.get_status("1")


async def test_async_get_post() -> None:
    client = AsyncCbmc()

    with aioresponses() as m:
        m.get(
            f"{client.base_url}/post/1",
            payload={
                "status": "success",
                "posts": {
                    "1": {
                        "post": {
                            "id": {"post": 1, "platform": 1},
                            "type": "靠北麥塊",
                            "content": "這是一篇靠北麥塊新站測試的第一篇文章\r\nhttps://cbmc.club/",
                            "photo": None,
                            "adminPost": True,
                            "approve": {
                                "time": "2021/11/12 19:17",
                                "timestamp": 1636715868,
                                "user": "單利",
                            },
                            "fbid": "924284348202766",
                        }
                    }
                },
            },
        )
        post = await client.get_post(1)

        assert post.post_id == 1
        assert post.platform_id == 1
        assert post.type == "靠北麥塊"
        assert post.content == "這是一篇靠北麥塊新站測試的第一篇文章\r\nhttps://cbmc.club/"
        assert post.__str__() == "這是一篇靠北麥塊新站測試的第一篇文章\r\nhttps://cbmc.club/"
        assert post.photo is None
        assert post.admin_post is True
        assert post.approve_timestamp == 1636715868
        assert post.approve_time == datetime.datetime(
            2021, 11, 12, 11, 17, 48, tzinfo=datetime.timezone.utc
        )
        assert post.approve_user == "單利"
        assert post.fbid == "924284348202766"
        assert post.__repr__() == "<Post post_id=1 platform_id=1>"
        assert post.to_dict() == {
            "post_id": 1,
            "platform_id": 1,
            "type": "靠北麥塊",
            "content": "這是一篇靠北麥塊新站測試的第一篇文章\r\nhttps://cbmc.club/",
            "photo": None,
            "admin_post": True,
            "approve_time": datetime.datetime(
                2021, 11, 12, 11, 17, 48, tzinfo=datetime.timezone.utc
            ),
            "approve_timestamp": 1636715868,
            "approve_user": "單利",
            "fbid": "924284348202766",
        }


async def test_async_get_post_not_found() -> None:
    client = AsyncCbmc()

    with aioresponses() as m:
        m.get(
            f"{client.base_url}/post/1",
            payload={"status": "failed", "message": "文章不存在、尚未經過審核或是被拒絕。"},
        )

        with raises(NotFound):
            await client.get_post(1)


async def test_async_get_post_http_exception() -> None:
    client = AsyncCbmc()

    with aioresponses() as m:
        m.get(f"{client.base_url}/post/1", status=500)

        with raises(HTTPException):
            await client.get_post(1)


async def test_async_get_post_type_error() -> None:
    client = AsyncCbmc()

    with raises(TypeError):
        await client.get_post("1")


async def test_async_get_posts() -> None:
    client = AsyncCbmc()

    with aioresponses() as m:
        m.get(
            f"{client.base_url}/latest?limit=2",
            payload={
                "status": "success",
                "limit": 2,
                "posts": {
                    "1": {
                        "post": {
                            "id": {"post": 1703, "platform": 2067},
                            "type": "靠北麥塊",
                            "content": "確定某瑞只有跑去開GTA嗎?\r\n\r\n搞不好換了個名字 繼續開騙錢服 準備再次惡意倒閉呢\r\n\r\n呵呵呵~~",
                            "photo": None,
                            "adminPost": False,
                            "approve": {
                                "time": "2023/04/24 14:20",
                                "timestamp": 1682317224,
                                "user": "凱能",
                            },
                            "fbid": "557710793137813",
                        }
                    },
                    "2": {
                        "post": {
                            "id": {"post": 1701, "platform": 2065},
                            "type": "靠北麥塊",
                            "content": "某瑞惡意倒閉莊x後，就跑去開GTA夜xx城，賺的幾百萬",
                            "photo": None,
                            "adminPost": False,
                            "approve": {
                                "time": "2023/04/18 19:32",
                                "timestamp": 1681817560,
                                "user": "奧莉安娜",
                            },
                            "fbid": "554633576778868",
                        }
                    },
                },
            },
        )

        posts = await client.get_posts(2)

        assert len(posts) == 2
        assert posts[0].post_id == 1703
        assert posts[0].platform_id == 2067
        assert posts[0].type == "靠北麥塊"
        assert posts[0].content == "確定某瑞只有跑去開GTA嗎?\r\n\r\n搞不好換了個名字 繼續開騙錢服 準備再次惡意倒閉呢\r\n\r\n呵呵呵~~"
        assert posts[0].__str__() == "確定某瑞只有跑去開GTA嗎?\r\n\r\n搞不好換了個名字 繼續開騙錢服 準備再次惡意倒閉呢\r\n\r\n呵呵呵~~"
        assert posts[0].photo is None
        assert posts[0].admin_post is False
        assert posts[0].approve_timestamp == 1682317224
        assert posts[0].approve_time == datetime.datetime(
            2023, 4, 24, 6, 20, 24, tzinfo=datetime.timezone.utc
        )
        assert posts[0].approve_user == "凱能"
        assert posts[0].fbid == "557710793137813"
        assert posts[0].__repr__() == "<Post post_id=1703 platform_id=2067>"
        assert posts[0].to_dict() == {
            "post_id": 1703,
            "platform_id": 2067,
            "type": "靠北麥塊",
            "content": "確定某瑞只有跑去開GTA嗎?\r\n\r\n搞不好換了個名字 繼續開騙錢服 準備再次惡意倒閉呢\r\n\r\n呵呵呵~~",
            "photo": None,
            "admin_post": False,
            "approve_time": datetime.datetime(2023, 4, 24, 6, 20, 24, tzinfo=datetime.timezone.utc),
            "approve_timestamp": 1682317224,
            "approve_user": "凱能",
            "fbid": "557710793137813",
        }


async def test_async_get_posts_http_exception() -> None:
    client = AsyncCbmc()

    with aioresponses() as m:
        m.get(f"{client.base_url}/latest?limit=2", status=500)

        with raises(HTTPException):
            await client.get_posts(2)


async def test_async_get_posts_type_error() -> None:
    client = AsyncCbmc()

    with raises(TypeError):
        await client.get_posts("2")


async def test_async_get_posts_value_error() -> None:
    client = AsyncCbmc()

    with raises(ValueError):
        await client.get_posts(0)

    with raises(ValueError):
        await client.get_posts(-1)

    with raises(ValueError):
        await client.get_posts(301)


async def test_async_get_status() -> None:
    client = AsyncCbmc()

    with raises(NotImplementedError):
        await client.get_status("1")
