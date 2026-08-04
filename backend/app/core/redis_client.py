from dotenv import load_dotenv
import os
import redis

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

redis_client = redis.Redis.from_url(REDIS_URL)