from flask import current_app, Flask
from werkzeug.local import LocalProxy

import redis


def create_redis_from(app: Flask):
    redis_url = app.config.get("REDIS_URL")
    redis_decode = app.config.get("REDIS_DECODE", False)
    if redis_url is None:
        raise RuntimeError("REDIS_URL is not configured")
    return redis.from_url(redis_url, decode_responses=redis_decode)


class RedisFlask():

    def __init__(self, app: Flask = None, redis: redis.Redis = None) -> None:
        self.redis = redis
        if app is not None:
            self.init_app(app)
        pass

    def init_app(self, app: Flask):
        if self.redis is None:
            self.redis = create_redis_from(app)

        app.extensions["redis_flask"] = self

        @app.teardown_appcontext
        def close(response_or_exc):
            if self.redis is not None:
                self.redis.close()
            pass
        pass
    pass


def _get_client():
    if "redis_flask" in current_app.extensions:
        return current_app.extensions["redis_flask"].redis

    key = "redis_client"
    if key not in current_app.extensions:
        current_app.extensions[key] = create_redis_from(current_app)
    return current_app.extensions[key]


redis_client: redis.Redis = LocalProxy(_get_client)
