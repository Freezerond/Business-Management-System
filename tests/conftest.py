import datetime

import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from backend.config import settings
from backend.database import Base, get_session
from backend.main import app
from backend.models.meetings import Meeting
from backend.models.tasks import TaskStatus
from backend.models.users import User, UserRole
from backend.schemas.evaluations import EvaluationCreateSchema
from backend.schemas.meetings import MeetingCreateSchema
from backend.schemas.tasks import TaskCreateSchema
from backend.services.evaluation_service import EvaluationService
from backend.services.jwt_manager import create_access_token
from backend.services.meeting_service import MeetingService
from backend.services.security import hash_password
from backend.services.task_service import TaskService
from backend.services.team_service import TeamService


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(settings.DB_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
def test_app(session):
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    return app


@pytest_asyncio.fixture
async def client(test_app):
    transport = ASGITransport(app=test_app)

    async with AsyncClient(
            transport=transport,
            base_url="http://test",
    ) as client:
        yield client


# -------------------- USERS --------------------

@pytest_asyncio.fixture
async def user(session):
    user = User(
        email="user@test.com",
        full_name="Test User",
        password=hash_password("password123"),
        role=UserRole.user
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest_asyncio.fixture
async def other_user(session):
    user = User(
        email="other@test.com",
        full_name="Other User",
        password=hash_password("password123"),
        role=UserRole.user
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture
def auth_headers(user):
    access_token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def auth_headers_other(other_user):
    access_token = create_access_token({"sub": str(other_user.id), "role": other_user.role.value})
    return {"Authorization": f"Bearer {access_token}"}


# -------------------- TEAMS --------------------

@pytest_asyncio.fixture
async def team(session, user):
    team = await TeamService.create_team(session, user, "Team")
    return team


@pytest_asyncio.fixture
async def team_with_member(session, user, other_user):
    team = await TeamService.create_team(session, user, "Team")
    await TeamService.add_user(session, user, user.team_id, other_user.id)
    return team


# -------------------- TASKS --------------------

@pytest_asyncio.fixture
async def task(session, team, user):
    return await TaskService.create_task(
        session,
        user,
        TaskCreateSchema(
            title="Task",
            description="Desc",
            deadline=None,
            executor_ids=[]
        )
    )


@pytest_asyncio.fixture
async def task_with_executor(session, team_with_member, user, other_user):
    return await TaskService.create_task(
        session,
        user,
        TaskCreateSchema(
            title="Task",
            description="Desc",
            deadline=None,
            executor_ids=[other_user.id]
        )
    )


@pytest_asyncio.fixture
async def done_task(session, task_with_executor):
    task_with_executor.status = TaskStatus.done
    await session.commit()
    return task_with_executor


# -------------------- EVALUATIONS --------------------


@pytest_asyncio.fixture
async def evaluation(session, user, other_user, done_task):
    eval_data = EvaluationCreateSchema(score=5, comment="Test", executor_id=other_user.id)
    return await EvaluationService.create_evaluation(session, user, done_task.id, eval_data)


# -------------------- MEETINGS --------------------

@pytest_asyncio.fixture
async def time_slot():
    start = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
    end = start + datetime.timedelta(hours=1)
    return start, end


@pytest_asyncio.fixture
async def meeting_with_participant(session, team_with_member, user, other_user, time_slot):
    start, end = time_slot
    meeting_data = MeetingCreateSchema(
        title="Team Meeting",
        description="Discuss tasks",
        start_time=start,
        end_time=end,
        participant_ids=[other_user.id]
    )
    return await MeetingService.create_meeting(session, user, meeting_data)

