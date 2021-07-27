
import sys

import redis as redis_lib

from Sophia import log
from Sophia.config import get_str_key

# Init Redis
redis = redis_lib.Redis(
    host=get_str_key("REDIS_URI"),
    port=get_str_key("REDIS_PORT"),
    password=get_str_key("REDIS_PASS"),
    decode_responses=True,
)

bredis = redis_lib.Redis(
    host=get_str_key("REDIS_URI"),
    port=get_str_key("REDIS_PORT"),
    password=get_str_key("REDIS_PASS"),
)

try:
    redis.ping()
except redis_lib.ConnectionError:
    sys.exit(log.critical("Can't connect to RedisDB! Exiting..."))
