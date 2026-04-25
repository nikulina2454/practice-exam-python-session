import os
import tempfile
from datetime import datetime, timedelta

from database.database_manager import DatabaseManager
from models.project import Project
from models.task import Task
from models.user import User


class TestDatabaseManager:
    def setup_method(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.db_manager.create_tables()

    def teardown_method(self):
        self.db_manager.close()
        os.unlink(self.temp_db.name)

    def test_create_tables_and_basic_crud(self):
        project_id = self.db_manager.add_project(
            Project("Проект", "Описание", datetime.now(), datetime.now() + timedelta(days=5))
        )
        user_id = self.db_manager.add_user(User("user", "user@example.com", "developer"))

        task_id = self.db_manager.add_task(
            Task(
                "Задача",
                "Описание",
                2,
                datetime.now() + timedelta(days=3),
                project_id,
                user_id,
            )
        )

        task = self.db_manager.get_task_by_id(task_id)
        assert task is not None
        assert task.title == "Задача"

        assert self.db_manager.update_task(task_id, status="completed") is True
        assert self.db_manager.get_task_by_id(task_id).status == "completed"

        assert len(self.db_manager.search_tasks("Задача")) == 1
        assert len(self.db_manager.get_tasks_by_project(project_id)) == 1
        assert len(self.db_manager.get_tasks_by_user(user_id)) == 1

        assert self.db_manager.delete_task(task_id) is True
        assert self.db_manager.get_task_by_id(task_id) is None
