from datetime import datetime
from typing import Optional

from sqlmodel import Field, Enum, Column
from sqlmodel.main import SQLModel

from ariadne_example.app.core.struсtures import TaskStatusEnum


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: Optional[str]
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = True


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow)
    title: str
    status: TaskStatusEnum = Field(sa_column=Column(Enum(TaskStatusEnum)), default=TaskStatusEnum.draft)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
