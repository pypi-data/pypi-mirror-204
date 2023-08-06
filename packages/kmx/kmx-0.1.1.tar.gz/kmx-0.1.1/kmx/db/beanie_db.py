from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from beanie.odm.documents import DocType

from kmx.flows.db import DbFlowRun, DbFlowTaskRun

class BeanieDbInitilizer:

    def __init__(self, mongo_url: str, db_name: str, document_models: list[DocType]):
        self.mongo_url = mongo_url
        self.db_name = db_name
        self.document_models = document_models

    async def init_db(self):
        """ """
        mongo_client = AsyncIOMotorClient(self.mongo_url, tz_aware=True)

        document_models = []
        document_models.extend(self.document_models)
        document_models.extend([DbFlowRun, DbFlowTaskRun])

        await init_beanie(database=mongo_client[self.db_name], document_models=document_models)
