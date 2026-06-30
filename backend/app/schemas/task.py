from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


TaskStatus = Literal["Todo", "In Progress", "Done"]


class TaskBase(BaseModel):
    """Shared fields between create and update schemas."""

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    status: TaskStatus = "Todo"


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task. All fields optional."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskResponse(TaskBase):
    """Schema for task data returned in API responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)