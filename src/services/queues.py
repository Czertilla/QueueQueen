from logging import getLogger
from uuid import UUID
from models.positions import PositionORM
from models.queues import QueueORM
from models.users import UserORM
from aiogram.types.user import User
from utils.absract.service import BaseService

logger = getLogger(__name__)

class QueueService(BaseService):
    async def check_username(self, value: str) -> bool:
        async with self.uow:
            self.uow.users.check_username(value)


    async def check_chat(self, chat_id: int, from_admin: bool = False) -> str:
        async with self.uow:
            queue = await self.uow.queues.get_by_chat_id(chat_id)
            if isinstance(queue, QueueORM):
                queue_data = await self.uow.queues.get_with_positions(queue.id)
                if isinstance(queue_data, QueueORM):
                    answer = f"Queue <code>{queue_data.id}</code>:"
                    queue_data.positions.sort(key =  lambda pos: pos.created_at)
                    if not len(queue_data.positions):
                        answer += "\n empty"
                    for p, pos in enumerate(queue_data.positions):
                        pos.position = p
                        answer += f"\n {pos.position} - {pos.user.first_name 
                                                         or ''} {pos.user.last_name or ''} (@{pos.user.username})"
            elif from_admin:
                queue_id = await self.uow.queues.add_one({
                    "chat_id": chat_id
                })
                if isinstance(queue_id, UUID):
                    answer = f"New queue created (id: <code>{queue_id}</code>)"
                else:
                    answer =  "some problem with creating new queue"
            else:
                return "no queue in this chat"
            await self.uow.commit(True)
        return answer
    

    async def add_user(self, user: User, chat_id: int) -> str:
        async with self.uow:
            queue = await self.uow.queues.get_by_chat_id(chat_id)
            if isinstance(queue, QueueORM):
                queue_data = await self.uow.queues.get_with_positions(queue.id)
                if isinstance(queue_data, QueueORM):
                    user_data = await self.uow.users.get_by_tgid(user.id)
                    if isinstance(user_data, UserORM):
                        if (l := await self.uow.queues.add_position(queue_data, user_data.id)) == -1:
                            return f"user @{user.username} already in queue"
                        else:
                            answer = f"@{user.username}, now your position is {l}"
                    else:
                        return "user not found"
            else:
                return "queue not found"
            await self.uow.commit(True)
        return answer
    

    async def remove_user(self, user: User, chat_id: int) -> tuple[str, int|None]:
        async with self.uow:
            queue = await self.uow.queues.get_by_chat_id(chat_id)
            if isinstance(queue, QueueORM):
                queue_data = await self.uow.queues.get_with_positions(queue.id)
                if isinstance(queue_data, QueueORM):
                    l = len(queue_data.positions)
                    user_data = await self.uow.users.get_by_tgid(user.id)
                    if isinstance(user_data, UserORM):
                        result = await self.uow.queues.remove_position(queue, user_data.id)
                        if not result[0]:
                            return f"user @{user.username} not in queue <code>{queue.id}</code>", None
                        else:
                            answer = f"user @{user.username} removed from queue <code>{queue.id}</code>"
                        notific_target = result[1]
                    else:
                        return "user not found", None
            else:
                return "queue not found", None
            await self.uow.commit(True)
        return answer, notific_target
            

    async def clear_queue(self, chat_id: int) -> str:
        async with self.uow:
            queue = await self.uow.queues.get_by_chat_id(chat_id)
            if isinstance(queue, QueueORM):
                await self.uow.queues.clear(queue.id)
                answer = f"the queue {queue.id} has been cleared"
            else:
                return "no queue in this chat"
            await self.uow.commit(True)
        return answer
