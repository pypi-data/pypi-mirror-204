from flask import current_app
from werkzeug.local import LocalProxy

import redis


def _get_client():
    key = "redis_client"
    if key not in current_app.extensions:
        config = current_app.config
        redis_url = config.get("REDIS_URL")
        if redis_url is None:
            raise RuntimeError("REDIS_URL is not configured")
        current_app.extensions[key] = redis.from_url(redis_url)
    return current_app.extensions[key]


redis_client: redis.Redis = LocalProxy(_get_client)
