from models.task import Task

class TaskController:
    def __init__(self, db_manager) -> None:
        self.db_manager = db_manager

    def add_task(self, title, description, priority, due_date, project_id, assignee_id) -> int:
        task = Task(title, description, priority, due_date, project_id, assignee_id)
        return self.db_manager.add_task(task)

    def get_task(self, task_id) -> Task | None:
        return self.db_manager.get_task_by_id(task_id)

    def get_all_tasks(self) -> list[Task]:
        return self.db_manager.get_all_tasks()

    def update_task(self, task_id, **kwargs) -> bool:
        return self.db_manager.update_task(task_id, **kwargs)

    def delete_task(self, task_id) -> bool:
        return self.db_manager.delete_task(task_id)

    def search_tasks(self, query) -> list[Task]:
        return self.db_manager.search_tasks(query)

    def update_task_status(self, task_id, new_status) -> bool:
        task = self.db_manager.get_task_by_id(task_id)
        if task is None:
            return False
        if not task.update_status(new_status):
            return False
        return self.db_manager.update_task(task_id, status=task.status)

    def get_overdue_tasks(self) -> list[Task]:
        return [task for task in self.db_manager.get_all_tasks() if task.is_overdue()]

    def get_tasks_by_project(self, project_id) -> list[Task]:
        return self.db_manager.get_tasks_by_project(project_id)

    def get_tasks_by_user(self, user_id) -> list[Task]:
        return self.db_manager.get_tasks_by_user(user_id)