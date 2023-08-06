import datetime
from enum import IntEnum

from pydantic import BaseModel, Field
from beanie import Document, Link, PydanticObjectId
import pymongo


class DbFlowRunState(IntEnum):
    """ """
    ACTIVE = 1
    FINISHED = 2


class DbFlowRun(Document):
    """ """
    uid: str  # уникальный идентификатор запуска

    flow_name: str
    state: DbFlowRunState

    context: dict = {}  # контекст выполнения потока

    delayed_until: datetime.datetime | None = None

    created_at: datetime.datetime
    finished_at: datetime.datetime | None = None

    class Settings:
        name = 'flow_runs'


class DbActiveFlowRunView(BaseModel):
    """ """
    id: PydanticObjectId = Field(alias="_id")
    uid: str
    flow_name: str
    delayed_until: datetime.datetime | None


class DbFlowTaskRunState(IntEnum):
    """ """
    ACTIVE = 1
    FINISHED = 2


class DbFlowTaskRun(Document):
    """ """

    flow_run_uid: str
    task_name: str

    state: DbFlowTaskRunState

    created_at: datetime.datetime
    finished_at: datetime.datetime | None

    class Settings:
        name = 'flow_task_runs'
        indexes = [
            [('flow_run_uid', pymongo.ASCENDING)],
        ]


class DbFinishedFlowTaskRunView(BaseModel):
    """ Проекция документа DbFlowTaskRun для запросов завершившихся задач """
    id: PydanticObjectId = Field(alias='_id')
    task_name: str
    state: DbFlowTaskRunState
