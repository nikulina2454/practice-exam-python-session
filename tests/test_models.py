from datetime import datetime, timedelta

import pytest

from models.project import Project
from models.task import Task
from models.user import User


def test_task_model_creation_and_methods():
    task = Task(
        title="Задача",
        description="Описание",
        priority=1,
        due_date=datetime.now() + timedelta(days=1),
        project_id=1,
        assignee_id=1,
    )
    assert task.status == "pending"
    assert task.update_status("in_progress") is True
    assert task.status == "in_progress"
    assert isinstance(task.to_dict(), dict)


def test_task_model_validation():
    with pytest.raises(ValueError):
        Task("", "Описание", 1, datetime.now(), 1, 1)

    with pytest.raises(ValueError):
        Task("Имя", "Описание", 7, datetime.now(), 1, 1)


def test_project_model_creation_and_methods():
    project = Project(
        name="Проект",
        description="Описание",
        start_date=datetime.now() - timedelta(days=2),
        end_date=datetime.now() + timedelta(days=2),
    )
    assert project.status == "active"
    assert project.update_status("completed") is True
    assert project.status == "completed"
    assert 0 <= project.get_progress() <= 100
    assert isinstance(project.to_dict(), dict)


def test_user_model_creation_and_methods():
    user = User("tester", "tester@example.com", "developer")
    assert user.username == "tester"
    user.update_info(username="tester2")
    assert user.username == "tester2"
    assert isinstance(user.to_dict(), dict)


def test_user_model_validation():
    with pytest.raises(ValueError):
        User("tester", "wrong-email", "developer")

    with pytest.raises(ValueError):
        User("tester", "tester@example.com", "unknown")
