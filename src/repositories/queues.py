from typing import AsyncGenerator
from uuid import UUID
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from database import BaseRepo
from logging import getLogger

from models.positions import PositionORM
from models.queues import QueueORM

logger = getLogger(__name__)

class QueueRepo(BaseRepo):
    model = QueueORM

    async def get_by_chat_id(self, chat_id: int) -> model|None:
        return (
            await self.execute(
                select(self.model)
                .where(self.model.chat_id == chat_id)
            )
        ).scalar_one_or_none()
    
    async def get_with_positions(self, id: UUID) -> model|None:
        return (
            await self.execute(
                select(self.model)
                .where(self.model.id == id)
                .options(selectinload(self.model.positions).joinedload(PositionORM.user))
            )
        ).scalar_one_or_none()
    

    async def get_position(self, queue_id: UUID, user_id: UUID) -> PositionORM:
        return (await self.execute(
            select(PositionORM)
            .where(PositionORM.queue_id == queue_id)
            .where(PositionORM.user_id == user_id)
        )).scalar_one_or_none()
    
    async def add_position(self, queue: model, user_id: UUID) -> int:
        if await self.get_position(queue.id, user_id):
            return -1
        queue.positions.append(PositionORM(queue_id = queue.id, user_id = user_id, position = (l:= len(queue.positions))))
        return l
    
    async def remove_position(self, queue: model, user_id: UUID) -> tuple[bool, int|None]:
        target = await self.get_position(queue.id, user_id)
        if not target:
            return (False, False)
        answer = (True, queue.positions[1].user.tgid if len(queue.positions) > 1 and target.position == 0 else None)
        await self.execute(
            delete(PositionORM)
            .where(PositionORM.queue_id == queue.id)
            .where(PositionORM.user_id == user_id))
        queue.positions.sort(key= lambda pos: pos.created_at)
        for p, position in enumerate(queue.positions):
            position.position = p
        return answer
    
    async def clear(self, queue_id: UUID) -> None:
        await self.execute(
            delete(PositionORM)
            .where(PositionORM.queue_id == queue_id)
        )
