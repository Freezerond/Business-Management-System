import pytest

from backend.schemas.evaluations import EvaluationCreateSchema, EvaluationUpdateSchema


# -------------------- CREATE EVALUATION --------------------

@pytest.mark.asyncio
async def test_create_evaluation_route(client, user, other_user, done_task, auth_headers):
    data = EvaluationCreateSchema(score=5, comment="Great", executor_id=other_user.id)

    response = await client.post(
        f"/evaluations/{done_task.id}",
        json=data.model_dump(),
        headers=auth_headers
    )

    assert response.status_code == 201
    json_data = response.json()
    assert json_data["score"] == 5
    assert json_data["comment"] == "Great"
    assert json_data["executor_id"] == other_user.id
    assert json_data["evaluator_id"] == user.id


@pytest.mark.asyncio
async def test_create_evaluation_forbidden_route(client, other_user, auth_headers_other, done_task):
    data = EvaluationCreateSchema(score=4, comment="Hack", executor_id=other_user.id)

    response = await client.post(
        f"/evaluations/{done_task.id}",
        headers=auth_headers_other,
        json=data.model_dump()
    )
    assert response.status_code == 403


# -------------------- GET EVALUATION --------------------

@pytest.mark.asyncio
async def test_get_evaluation_route(client, other_user, evaluation, auth_headers):
    response = await client.get(
        f"/evaluations/{evaluation.task_id}/{other_user.id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["score"] == 5
    assert json_data["executor_id"] == other_user.id


# -------------------- UPDATE EVALUATION --------------------

@pytest.mark.asyncio
async def test_update_evaluation_route(client, other_user, evaluation, auth_headers):
    update_data = EvaluationUpdateSchema(score=4, comment="Updated")
    response = await client.patch(
        f"/evaluations/{evaluation.task_id}/{other_user.id}",
        headers=auth_headers,
        json=update_data.model_dump(exclude_unset=True)
    )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["score"] == 4
    assert json_data["comment"] == "Updated"


# -------------------- DELETE EVALUATION --------------------

@pytest.mark.asyncio
async def test_delete_evaluation_route(client, other_user, evaluation, auth_headers):
    response = await client.delete(
        f"/evaluations/{evaluation.task_id}/{other_user.id}",
        headers=auth_headers
    )
    assert response.status_code == 204


# -------------------- GET MY GIVEN --------------------

@pytest.mark.asyncio
async def test_get_my_given_route(client, other_user, evaluation, auth_headers):
    response = await client.get(
        "/evaluations/my_given",
        headers=auth_headers
    )
    assert response.status_code == 200
    json_data = response.json()
    assert any(e["executor_id"] == other_user.id for e in json_data)


# -------------------- GET MY RECEIVED --------------------

@pytest.mark.asyncio
async def test_get_my_received_route(client, other_user, auth_headers_other, evaluation):
    response = await client.get(
        "/evaluations/my_received",
        headers=auth_headers_other
    )
    assert response.status_code == 200
    json_data = response.json()
    assert any(e["executor_id"] == other_user.id for e in json_data)


# -------------------- GET AVERAGE --------------------

@pytest.mark.asyncio
async def test_get_average_route(client, other_user, evaluation, auth_headers):
    response = await client.get(
        f"/evaluations/average?user_id={other_user.id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["user_id"] == other_user.id
    assert json_data["count"] == 1
    assert json_data["average_score"] == 5
