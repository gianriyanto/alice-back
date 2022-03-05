import logging

import asyncio
from motor import motor_asyncio

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


CONN_STR = "mongodb+srv://alice:alice@cluster0.1oby8.mongodb.net/alice?retryWrites=true&w=majority"


async def get_server_info():
    logger.info("Attempting to establish a database connection")
    client = motor_asyncio.AsyncIOMotorClient(CONN_STR, 5000)

    try:
        logger.info(await client.server_info())
    except Exception:
        logger.warning("Unable to establish a connection with the database")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_server_info())


# if __name__ == "__main__":
#     client = pymongo.MongoClient("mongodb+srv://alice:<password>@cluster0.1oby8.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#     db = client.test
#     print(db)
