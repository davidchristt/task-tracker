from typing import Optional

from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks(db: Session) -> list[Task]:
    """Retrieve all tasks ordered by creation date (newest first)."""
    return db.query(Task).order_by(Task.created_at.desc()).all()


def get_task(db: Session, task_id: int) -> Optional[Task]:
    """Retrieve a single task by ID. Returns None if not found."""
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, task_data: TaskCreate) -> Task:
    """Create a new task in the database."""
    new_task = Task(**task_data.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task(
    db: Session, task_id: int, task_data: TaskUpdate
) -> Optional[Task]:
    """Update an existing task. Returns updated task, or None if not found."""
    task = get_task(db, task_id)
    if task is None:
        return None

    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> bool:
    """Delete a task by ID. Returns True if deleted, False if not found."""
    task = get_task(db, task_id)
    if task is None:
        return False

    db.delete(task)
    db.commit()
    return True