from fastapi import FastAPI, HTTPException
from typing import List
from models import User, Gender, Roles, UUID, UserUpdateRequest
from uuid import uuid4

app = FastAPI()

db: List[User] = [
    User(
        id=uuid4(),
        first_name="John",
        last_name="Doe",
        gender = Gender.female,
        roles = [Roles.user]
    ),
    User(
        id=uuid4(),
        first_name="Anna",
        last_name="Clara",
        gender=Gender.female,
        roles=[Roles.user]
    )
]


@app.get("/")
async def root():
    return {"message": "Hello Mundo"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def create_user(user: User):
    user.id = uuid4()
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message": "User deleted"}
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is None:
                user.first_name = user_update.first_name
            if user_update.last_name is None:
                user.last_name = user_update.last_name
            if user_update.middle_name is None:
                user.middle_name = user_update.middle_name
            if user_update.roles is None:
                user.roles = user_update.roles
            return {"message": "User updated"}
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )
