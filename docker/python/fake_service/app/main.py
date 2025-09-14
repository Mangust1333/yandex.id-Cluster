import uvicorn
from fastapi import FastAPI, HTTPException, Query
from typing import List
from uuid import UUID

from .db import init_db_pool, close_db_pool
from .queries import (
    fetch_user_profile,
    fetch_device_activity,
    fetch_open_support_sessions,
    fetch_group_transactions,
    fetch_admins_activity,
    import_db_pool
)

app = FastAPI(
    title="UserService API",
    description="Пример сервисных эндпойнтов для работы с таблицами",
    version="1.0.0"
)

@app.on_event("startup")
async def on_startup():
    await init_db_pool()
    import_db_pool()

@app.on_event("shutdown")
async def on_shutdown():
    await close_db_pool()


@app.get("/health", summary="Проверка статуса сервиса")
async def health_check():
    return {"status": "OK"}


@app.get(
    "/api/v1/users/{user_id}/profile",
    summary="Развёрнутый профиль пользователя",
    response_model=List[dict]
)
async def get_user_profile(user_id: UUID):
    rows = await fetch_user_profile(user_id)
    if not rows:
        raise HTTPException(status_code=404, detail="User not found")
    return rows


@app.get(
    "/api/v1/devices/{device_id}/activity",
    summary="История активности устройства (за 7 дней)",
    response_model=List[dict]
)
async def get_device_activity(device_id: UUID):
    rows = await fetch_device_activity(device_id)
    return rows


@app.get(
    "/api/v1/support-sessions/{agent_id}/open",
    summary="Открытые сессии поддержки для агента",
    response_model=List[dict]
)
async def get_open_support_sessions(agent_id: UUID):
    rows = await fetch_open_support_sessions(agent_id)
    return rows


@app.get(
    "/api/v1/family-groups/{group_id}/transactions",
    summary="Транзакции успешного типа за последний месяц для группы пользователей",
    response_model=List[dict]
)
async def get_group_transactions(group_id: UUID):
    rows = await fetch_group_transactions(group_id)
    return rows


@app.get(
    "/api/v1/admins/activity",
    summary="Администраторы с количеством действий > min_actions за 30 дней",
    response_model=List[dict]
)
async def get_admins_activity():
    rows = await fetch_admins_activity()
    print("Запрос выполнен2!!!")
    print(rows)
    return rows


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
