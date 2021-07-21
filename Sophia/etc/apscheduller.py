from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from Sophia.config import get_str_key
from Sophia.utils.logger import log

DEFAULT = "default"

jobstores = {
    DEFAULT: RedisJobStore(
        host=get_str_key("REDIS_URI"),
        port=get_str_key("REDIS_PORT"),
        password=get_str_key("REDIS_PASS"),
    )
}
executors = {DEFAULT: AsyncIOExecutor()}
job_defaults = {"coalesce": False, "max_instances": 3}

scheduler = AsyncIOScheduler(
    jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc
)

log.info("Starting apscheduller...")
scheduler.start()
