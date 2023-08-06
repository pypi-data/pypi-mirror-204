from typing import NamedTuple
from collections import namedtuple


__CacheKeys = namedtuple(
    "CacheKeys",
    [
        "STREAM_ERROR_KEY_PREFIX",  # Error stream key
        "STREAM_SUCCESS_KEY_PREFIX",  # Success stream key
        "STREAM_REVIEW_KEY",  # Stream key for review events
        "STREAM_VENDORPAGE_KEY",  # Stream key for vendor page events
    ],
)


cache_keys = __CacheKeys("event_error", "event_success", "review", "vendor_page")
