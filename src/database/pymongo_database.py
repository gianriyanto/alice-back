import pymongo
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


CONN_STR = "mongodb+srv://alice:alice@cluster0.1oby8.mongodb.net/alice?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONN_STR, serverSelectionTimeoutMS=10000)
db = client["alice"]


def get_server():
    try:
        server_info = client.server_info()
        logger.info(f"""Successfully established a connection with the server {server_info["version"]}""")
        return server_info
    except Exception:
        logger.info("Unable to connect to the server.")


if __name__ == "__main__":
    logger.info(get_server())
