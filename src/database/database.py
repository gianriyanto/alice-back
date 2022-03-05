import asyncio
import motor.motor_asyncio
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


CONN_STR = "mongodb+srv://alice:alice@cluster0.1oby8.mongodb.net/alice?retryWrites=true&w=majority"


class DatabaseManager:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.client = motor.motor_asyncio.AsyncIOMotorClient(CONN_STR, io_loop=self.loop)

    async def get_server_info(self):
        try:
            logger.info(self.client.server_info())
        except Exception:
            logger.info("Unable to connect to the server.")

    # async def insert_to_database(self, product):
    #     await self.client.ProjektProducts.produkty.insert_one(product)
    #
    # async def get_products(self):
    #     db = self.client.test
    #     collection = db.products
    #     object = await collection.find_one({"song": "Young Thug - Relationship"})
    #     for objects in object:
    #         print(objects)
    #
    # def update_products(self):
    #     collection = self.client.test.products
    #     collection.update_one({'song': 'exampletitle'}, {"$set": {'is_awesome': "indeed"}})


db = DatabaseManager()
db.loop.close()


if __name__ == "__main__":
    db.loop.run_until_complete(db.get_server_info())
