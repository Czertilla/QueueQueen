from random import randint
import pytest
import asyncio
from unittest.mock import AsyncMock
from uuid import uuid4
from schemas.queues import SQueueList, SAddUserResponse, SRemoveUserResponse
from schemas.users import SUser
from services.queues import QueueService
from models.queues import QueueORM
from models.positions import PositionORM
from models.users import UserORM


@pytest.fixture
def queue_service():
    uow_mock = AsyncMock()
    return QueueService(uow=uow_mock)


def gen_user():
    return SUser(
        id=(id := uuid4()),
        tgid=randint(600000000, 800000000),
        username=str(id),
        first_name="test_user",
        is_bot=False
    )


@pytest.mark.asyncio
async def test_get_queue_list(queue_service: QueueService):
    chat_id = 12345
    queue_id = uuid4()
    user = gen_user()
    position = PositionORM(user=UserORM(**user.model_dump()), created_at=1)
    queue = QueueORM(id=queue_id, chat_id=chat_id, positions=[position])

    queue_service.uow.queues.get_by_chat_id = AsyncMock(return_value=queue)
    queue_service.uow.queues.get_with_positions = AsyncMock(return_value=queue)

    result = await queue_service.get_queue_list(chat_id)

    assert isinstance(result, SQueueList)
    assert result.id == queue_id
    assert len(result.positions) == 1
    assert result.positions[0].id == user.id
    assert result.is_new is False


@pytest.mark.asyncio
async def test_get_queue_list_create(queue_service: QueueService):
    chat_id = 12345
    queue_service.uow.queues.get_by_chat_id = AsyncMock(return_value=None)
    queue_service.uow.queues.add_one = AsyncMock(
        return_value=(queue_id := uuid4()))

    result = await queue_service.get_queue_list(chat_id, True)

    assert isinstance(result, SQueueList)
    assert result.id == queue_id
    assert result.positions == []
    assert result.is_new is True


@pytest.mark.asyncio
async def test_get_queue_list_no_queue(queue_service: QueueService):
    chat_id = 12345
    queue_service.uow.queues.get_by_chat_id = AsyncMock(return_value=None)

    result = await queue_service.get_queue_list(chat_id)

    assert isinstance(result, SQueueList)
    assert result.id is None
    assert result.positions is None
    assert result.is_new is False


@pytest.mark.asyncio
async def test_add_user(queue_service: QueueService):
    chat_id = 12345
    queue_id = uuid4()
    user = gen_user()
    queue = QueueORM(id=queue_id, chat_id=chat_id, positions=[])

    queue_service.uow.queues.get_by_chat_id = AsyncMock(return_value=queue)
    queue_service.uow.queues.get_with_positions = AsyncMock(return_value=queue)
    queue_service.uow.users.check_existence = AsyncMock(return_value=True)
    queue_service.uow.queues.add_position = AsyncMock(return_value=1)

    result = await queue_service.add_user(user, chat_id)

    assert isinstance(result, SAddUserResponse)
    assert result.queue_id == queue_id
    assert result.user == user
    assert result.position == 1


@pytest.mark.asyncio
async def test_add_user_no_queue(queue_service: QueueService):
    chat_id = 12345
    user = gen_user()

    queue_service.uow.queues.get_by_chat_id = AsyncMock(return_value=None)
    queue_service.uow.queues.get_with_positions = AsyncMock(return_value=None)
    queue_service.uow.users.check_existence = AsyncMock(return_value=True)
    queue_service.uow.queues.add_position = AsyncMock(return_value=None)

    result = await queue_service.add_user(user, chat_id)

    assert isinstance(result, SAddUserResponse)
    assert result.queue_id == None
    assert result.user == user
    assert result.is_already is False
    assert result.position == -1


@pytest.mark.asyncio
async def test_add_user_no_user(queue_service: QueueService):
    chat_id = 12345
    queue_id = uuid4()
    user = gen_user()
    queue = QueueORM(id=queue_id, chat_id=chat_id, positions=[])

    queue_service.uow.queues.get_by_chat_id = AsyncMock(return_value=queue)
    queue_service.uow.queues.get_with_positions = AsyncMock(return_value=queue)
    queue_service.uow.users.check_existence = AsyncMock(return_value=False)
    queue_service.uow.queues.add_position = AsyncMock(return_value=None)

    result = await queue_service.add_user(user, chat_id)

    assert isinstance(result, SAddUserResponse)
    assert result.queue_id == queue_id
    assert result.user == None
    assert result.is_already is False
    assert result.position == -1


@pytest.mark.asyncio
async def test_add_user_already_in_queue(queue_service: QueueService):
    chat_id = 12345
    queue_id = uuid4()
    user = gen_user()
    queue = QueueORM(id=queue_id, chat_id=chat_id, positions=[])

    queue_service.uow.queues.get_by_chat_id = AsyncMock(return_value=queue)
    queue_service.uow.queues.get_with_positions = AsyncMock(return_value=queue)
    queue_service.uow.users.check_existence = AsyncMock(return_value=True)
    queue_service.uow.queues.add_position = AsyncMock(return_value=-1)

    result = await queue_service.add_user(user, chat_id)

    assert isinstance(result, SAddUserResponse)
    assert result.queue_id == queue_id
    assert result.user == user
    assert result.is_already is True
    assert result.position == -1


@pytest.mark.asyncio
async def test_remove_user(queue_service: QueueService):
    chat_id = 12345
    queue_id = uuid4()
    user1 = gen_user()
    user2 = gen_user()
    position1 = PositionORM(
        id=uuid4(), queue_id=queue_id, user=UserORM(**user1.model_dump()))
    position2 = PositionORM(
        id=uuid4(), queue_id=queue_id, user=UserORM(**user2.model_dump()))
    queue = QueueORM(
        id=queue_id, chat_id=chat_id, positions=[position1, position2])

    queue_service.uow.queues.get_by_chat_id = AsyncMock(return_value=queue)
    queue_service.uow.queues.get_with_positions = AsyncMock(return_value=queue)
    queue_service.uow.users.check_existence = AsyncMock(return_value=True)
    queue_service.uow.queues.remove_position = AsyncMock(
        return_value=(True, user2.tgid))

    queue.positions.pop(0)

    result = await queue_service.remove_user(user1, chat_id)

    assert isinstance(result, SRemoveUserResponse)
    assert result.queue_id == queue_id
    assert result.user == user1
    assert result.is_already is False
    assert result.notificate_target == user2.tgid

    queue_service.uow.users.check_existence = AsyncMock(return_value=True)
    queue_service.uow.queues.remove_position = AsyncMock(
        return_value=(True, None))

    result = await queue_service.remove_user(user2, chat_id)

    assert isinstance(result, SRemoveUserResponse)
    assert result.queue_id == queue_id
    assert result.user == user2
    assert result.is_already is False
    assert result.notificate_target is None


@pytest.mark.asyncio
async def test_remove_user_no_queue(queue_service: QueueService):
    chat_id = 12345
    user = gen_user()

    queue_service.uow.queues.get_by_chat_id = AsyncMock(return_value=None)
    queue_service.uow.queues.get_with_positions = AsyncMock(return_value=None)
    queue_service.uow.users.check_existence = AsyncMock(return_value=True)
    queue_service.uow.queues.remove_position = AsyncMock(
        return_value=(False, None))

    result = await queue_service.remove_user(user, chat_id)

    assert isinstance(result, SRemoveUserResponse)
    assert result.queue_id == None
    assert result.user == user
    assert result.is_already is False


@pytest.mark.asyncio
async def test_remove_user_not_in_queue(queue_service: QueueService):
    chat_id = 12345
    queue_id = uuid4()
    user = gen_user()
    queue = QueueORM(id=queue_id, chat_id=chat_id, positions=[])

    queue_service.uow.queues.get_by_chat_id = AsyncMock(return_value=queue)
    queue_service.uow.queues.get_with_positions = AsyncMock(return_value=queue)
    queue_service.uow.users.check_existence = AsyncMock(return_value=True)
    queue_service.uow.queues.remove_position = AsyncMock(
        return_value=(False, None))

    result = await queue_service.remove_user(user, chat_id)

    assert isinstance(result, SRemoveUserResponse)
    assert result.queue_id == queue_id
    assert result.user == user
    assert result.is_already is True


@pytest.mark.asyncio
async def test_clear_queue(queue_service: QueueService):
    chat_id = 12345
    queue_id = uuid4()
    queue = QueueORM(id=queue_id, chat_id=chat_id, positions=[])

    queue_service.uow.queues.get_by_chat_id = AsyncMock(return_value=queue)

    result = await queue_service.clear_queue(chat_id)

    assert result == queue_id


@pytest.mark.asyncio
async def test_clear_queue_no_queue(queue_service: QueueService):
    chat_id = 12345
    queue_service.uow.queues.get_by_chat_id = AsyncMock(return_value=None)

    result = await queue_service.clear_queue(chat_id)

    assert result is None


@pytest.mark.asyncio
async def test_check_position_queue_not_found(queue_service: QueueService):
    queue_service.uow.queues.get_by_chat_id = AsyncMock(return_value=None)

    result = await queue_service.check_position(target="1", chat_id=123)

    assert result is not None
    assert result.user is None
    assert result.queue_id is None


@pytest.mark.asyncio
async def test_check_position_valid_index(queue_service: QueueService):
    chat_id = 12345
    queue_id = uuid4()
    user = gen_user()
    position = PositionORM(
        user=(userORM := UserORM(**user.model_dump())), created_at=1
    )
    queue = QueueORM(id=queue_id, chat_id=chat_id, positions=[position])
    queue_service.uow.queues.get_by_chat_id = AsyncMock(
        return_value=queue)
    queue_service.uow.queues.get_with_positions = AsyncMock(
        return_value=queue)
    queue_service.uow.users.get = AsyncMock(return_value=userORM)

    result = await queue_service.check_position(target="0", chat_id=chat_id)

    assert result is not None
    assert result.user.id == user.id
    assert result.queue_id == queue.id


@pytest.mark.asyncio
async def test_check_position_invalid_index(queue_service: QueueService):
    chat_id = 12345
    queue_id = uuid4()
    queue = QueueORM(id=queue_id, chat_id=chat_id, positions=[])
    queue_service.uow.queues.get_by_chat_id = AsyncMock(
        return_value=queue)
    queue_service.uow.queues.get_with_positions = AsyncMock(
        return_value=queue)

    result = await queue_service.check_position(target="100", chat_id=chat_id)

    assert result is not None
    assert result.user is None
    assert result.queue_id == queue.id


@pytest.mark.asyncio
async def test_check_position_valid_username(queue_service: QueueService):
    chat_id = 12345
    queue_id = uuid4()
    user = gen_user()
    position1 = PositionORM(
        id=uuid4(),
        queue_id=queue_id,
        user=(userORM := UserORM(**user.model_dump()))
    )
    queue = QueueORM(
        id=queue_id, chat_id=chat_id, positions=[position1])

    queue_service.uow.queues.get_by_chat_id = AsyncMock(
        return_value=queue)
    queue_service.uow.queues.get_with_positions = AsyncMock(
        return_value=queue)
    queue_service.uow.users.get_by_username = AsyncMock(return_value=userORM)

    result = await queue_service.check_position(target=user.username, chat_id=chat_id)

    assert result is not None
    assert result.user.id == user.id
    assert result.queue_id == queue.id


@pytest.mark.asyncio
async def test_check_position_unknown_username(queue_service: QueueService):
    chat_id = 12345
    queue_id = uuid4()
    user = gen_user()
    position1 = PositionORM(
        id=uuid4(), queue_id=queue_id, user=UserORM(**user.model_dump()))
    queue = QueueORM(
        id=queue_id, chat_id=chat_id, positions=[position1])

    queue_service.uow.queues.get_by_chat_id = AsyncMock(
        return_value=queue)
    queue_service.uow.queues.get_with_positions = AsyncMock(
        return_value=queue)
    queue_service.uow.users.get_by_username = AsyncMock(return_value=None)


    result = await queue_service.check_position(target="unknown_user", chat_id=chat_id)

    assert result is not None
    assert result.user is None
    assert result.queue_id == queue.id


@pytest.mark.asyncio
async def test_check_position_multiple_positions_error(
    queue_service: QueueService
):
    chat_id = 12345
    queue_id = uuid4()
    user = gen_user()
    position1 = PositionORM(
        id=uuid4(),
        queue_id=queue_id,
        user_id = user.id,
        user=(userORM := UserORM(**user.model_dump()))
    )
    position2 = PositionORM(
        id=uuid4(),
        queue_id=queue_id,
        user_id = user.id,
        user=(userORM)
    )
    queue = QueueORM(
        id=queue_id, chat_id=chat_id, positions=[position1, position2])

    queue_service.uow.queues.get_by_chat_id = AsyncMock(
        return_value=queue)
    queue_service.uow.queues.get_with_positions = AsyncMock(
        return_value=queue)
    queue_service.uow.users.get_by_username = AsyncMock(return_value=userORM)

    result = await queue_service.check_position(target=user.username, chat_id=chat_id)

    assert result is None  # Ошибка должна вернуть None
