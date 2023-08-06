# cbmc.py

<!-- Add a badge here -->

[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)](https://pypi.org/project/cbmc.py/)
[![CodeFactor](https://www.codefactor.io/repository/github/itsrqtl/cbmc.py/badge)](https://www.codefactor.io/repository/github/itsrqtl/cbmc.py)

[![PyPI](https://img.shields.io/pypi/v/cbmc.py)](https://pypi.org/project/cbmc.py/)
[![PyPI - License](https://img.shields.io/pypi/l/cbmc.py)](https://pypi.org/project/cbmc.py/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/cbmc.py)](https://pypi.org/project/cbmc.py/)

Unofficial 麥塊匿名發文平台 API Wrapper for Python

## Installation

```sh
pip install cbmc.py
```

## Usage

```py
# Import the library
from cbmc import AsyncCbmc, SyncCbmc

# Obtain post with post id, raise cbmc.NotFound if not found
SyncCbmc.get_post(1)

# List recent posts, maximum 300 posts.
SyncCbmc.get_posts()

# Also available in async
async def main():
    await AsyncCbmc.get_post(1)
    await AsyncCbmc.get_posts()
```
