import logging
import asyncio
from motor import motor_asyncio

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


CONN_STR = "mongodb+srv://alice:alice@cluster0.1oby8.mongodb.net/alice?retryWrites=true&w=majority"
db = motor_asyncio.AsyncIOMotorClient(CONN_STR, 5000)


async def get_server_info():
    try:
        logger.info(await db.server_info())
    except Exception:
        logger.warning("Unable to establish a connection with the database")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_server_info())
    loop.close()
