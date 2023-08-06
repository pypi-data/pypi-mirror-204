import logging

from .bot import Bot
from .config import BOT_TOKEN, MONGO
from .deps import MongoStorage, Update
from .dispatcher import Dispatcher

bot = Bot(BOT_TOKEN)

storage = MongoStorage(
    db_name=MONGO.DB,
    host=MONGO.HOST,
    username=MONGO.USER,
    password=MONGO.PASSWORD,
)

dp = Dispatcher(bot, storage=storage)
logger = logging.getLogger()


@dp.errors_handler()
async def _(update: Update, error: Exception):
    logger.exception(f"{error=} on {update=}")
    return True
