import os
import tempfile
from datetime import datetime, timedelta

from controllers.project_controller import ProjectController
from controllers.task_controller import TaskController
from controllers.user_controller import UserController
from database.database_manager import DatabaseManager


class TestControllers:
    def setup_method(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.db_manager.create_tables()
        self.project_controller = ProjectController(self.db_manager)
        self.task_controller = TaskController(self.db_manager)
        self.user_controller = UserController(self.db_manager)

    def teardown_method(self):
        self.db_manager.close()
        os.unlink(self.temp_db.name)

    def test_controller_integration(self):
        project_id = self.project_controller.add_project(
            "Проект",
            "Описание",
            datetime.now(),
            datetime.now() + timedelta(days=14),
        )
        user_id = self.user_controller.add_user("dev", "dev@example.com", "developer")

        task_id = self.task_controller.add_task(
            "Задача",
            "Описание",
            1,
            datetime.now() + timedelta(days=2),
            project_id,
            user_id,
        )
        assert self.task_controller.get_task(task_id) is not None

        assert self.task_controller.update_task_status(task_id, "in_progress") is True
        assert self.task_controller.get_task(task_id).status == "in_progress"

        assert len(self.user_controller.get_user_tasks(user_id)) == 1
        assert len(self.task_controller.get_tasks_by_project(project_id)) == 1
        assert 0 <= self.project_controller.get_project_progress(project_id) <= 100
