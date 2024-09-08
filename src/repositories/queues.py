from typing import AsyncGenerator
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import new_session, BaseRepo
from logging import getLogger

from models.queues import QueueORM
from models.users import UserORM

logger = getLogger(__name__)

class QueueRepo(BaseRepo):
    model = QueueORM

    ...