import pymongo
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


CONN_STR = "mongodb+srv://alice:alice@cluster0.1oby8.mongodb.net/alice?retryWrites=true&w=majority"
db = pymongo.MongoClient(CONN_STR, serverSelectionTimeoutMS=5000)


def get_server():
    # TODO Add test db connection in readiness check
    try:
        logger.info(db.server_info())
    except Exception:
        logger.info("Unable to connect to the server.")


if __name__ == "__main__":
    get_server()
