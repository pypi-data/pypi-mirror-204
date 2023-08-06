import datetime

from pytest import raises

from cbmc.post import Post


def test_post_missing() -> None:
    with raises(TypeError):
        Post()


def test_empty_post() -> None:
    post = Post({})

    assert post.post_id is None
    assert post.platform_id is None
    assert post.type is None
    assert post.content is None
    assert post.__str__() is None
    assert post.photo is None
    assert post.admin_post is None
    assert post.approve_timestamp is None
    assert post.approve_time is None
    assert post.approve_user is None
    assert post.fbid is None
    assert post.__repr__() == "<Post post_id=None platform_id=None>"
    assert post.to_dict() == {
        "post_id": None,
        "platform_id": None,
        "type": None,
        "content": None,
        "photo": None,
        "admin_post": None,
        "approve_time": None,
        "approve_timestamp": None,
        "approve_user": None,
        "fbid": None,
    }


def test_post() -> None:
    post = Post(
        {
            "id": {"post": 1, "platform": 1},
            "type": "靠北麥塊",
            "content": "Hello, world!",
            "photo": None,
            "adminPost": False,
            "approve": {"time": "1970/01/01 08:00", "timestamp": 0, "user": "user"},
            "fbid": "https://www.facebook.com/1234567890/posts/1234567890123456",
        }
    )

    assert post.post_id == 1
    assert post.platform_id == 1
    assert post.type == "靠北麥塊"
    assert post.content == "Hello, world!"
    assert post.__str__() == "Hello, world!"
    assert post.photo is None
    assert post.admin_post is False
    assert post.approve_timestamp == 0
    assert post.approve_time == datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
    assert post.approve_user == "user"
    assert post.fbid == "https://www.facebook.com/1234567890/posts/1234567890123456"
    assert post.__repr__() == "<Post post_id=1 platform_id=1>"
    assert post.to_dict() == {
        "post_id": 1,
        "platform_id": 1,
        "type": "靠北麥塊",
        "content": "Hello, world!",
        "photo": None,
        "admin_post": False,
        "approve_time": datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        "approve_timestamp": 0,
        "approve_user": "user",
        "fbid": "https://www.facebook.com/1234567890/posts/1234567890123456",
    }


def test_post_with_photo() -> None:
    post = Post(
        {
            "id": {"post": 1, "platform": 1},
            "type": "靠北麥塊",
            "content": "Hello, world!",
            "photo": "https://example.com/image.jpg",
            "adminPost": False,
            "approve": {"time": "1970/01/01 08:00", "timestamp": 0, "user": "user"},
            "fbid": "https://www.facebook.com/1234567890/posts/1234567890123456",
        }
    )

    assert post.post_id == 1
    assert post.platform_id == 1
    assert post.type == "靠北麥塊"
    assert post.content == "Hello, world!"
    assert post.__str__() == "Hello, world!"
    assert post.photo == "https://example.com/image.jpg"
    assert post.admin_post is False
    assert post.approve_timestamp == 0
    assert post.approve_time == datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
    assert post.approve_user == "user"
    assert post.fbid == "https://www.facebook.com/1234567890/posts/1234567890123456"
    assert post.__repr__() == "<Post post_id=1 platform_id=1>"
    assert post.to_dict() == {
        "post_id": 1,
        "platform_id": 1,
        "type": "靠北麥塊",
        "content": "Hello, world!",
        "photo": "https://example.com/image.jpg",
        "admin_post": False,
        "approve_time": datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        "approve_timestamp": 0,
        "approve_user": "user",
        "fbid": "https://www.facebook.com/1234567890/posts/1234567890123456",
    }


def test_post_missing_approve_timestamp() -> None:
    post = Post(
        {
            "id": {"post": 1, "platform": 1},
            "type": "靠北麥塊",
            "content": "Hello, world!",
            "photo": None,
            "adminPost": False,
            "approve": {"user": "user"},
            "fbid": "https://www.facebook.com/1234567890/posts/1234567890123456",
        }
    )

    assert post.post_id == 1
    assert post.platform_id == 1
    assert post.type == "靠北麥塊"
    assert post.content == "Hello, world!"
    assert post.__str__() == "Hello, world!"
    assert post.photo is None
    assert post.admin_post is False
    assert post.approve_timestamp is None
    assert post.approve_time is None
    assert post.approve_user == "user"
    assert post.fbid == "https://www.facebook.com/1234567890/posts/1234567890123456"
    assert post.__repr__() == "<Post post_id=1 platform_id=1>"
    assert post.to_dict() == {
        "post_id": 1,
        "platform_id": 1,
        "type": "靠北麥塊",
        "content": "Hello, world!",
        "photo": None,
        "admin_post": False,
        "approve_time": None,
        "approve_timestamp": None,
        "approve_user": "user",
        "fbid": "https://www.facebook.com/1234567890/posts/1234567890123456",
    }


def test_admin_post() -> None:
    post = Post(
        {
            "id": {"post": 1, "platform": 1},
            "type": "靠北麥塊",
            "content": "Hello, world!",
            "photo": None,
            "adminPost": True,
            "approve": {"time": "1970/01/01 08:00", "timestamp": 0, "user": "user"},
            "fbid": "https://www.facebook.com/1234567890/posts/1234567890123456",
        }
    )

    assert post.post_id == 1
    assert post.platform_id == 1
    assert post.type == "靠北麥塊"
    assert post.content == "Hello, world!"
    assert post.__str__() == "Hello, world!"
    assert post.photo is None
    assert post.admin_post is True
    assert post.approve_timestamp == 0
    assert post.approve_time == datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
    assert post.approve_user == "user"
    assert post.fbid == "https://www.facebook.com/1234567890/posts/1234567890123456"
    assert post.__repr__() == "<Post post_id=1 platform_id=1>"
    assert post.to_dict() == {
        "post_id": 1,
        "platform_id": 1,
        "type": "靠北麥塊",
        "content": "Hello, world!",
        "photo": None,
        "admin_post": True,
        "approve_time": datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        "approve_timestamp": 0,
        "approve_user": "user",
        "fbid": "https://www.facebook.com/1234567890/posts/1234567890123456",
    }
