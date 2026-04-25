from models.project import Project

class ProjectController:
    def __init__(self, db_manager) -> None:
        self.db_manager = db_manager

    def add_project(self, name, description, start_date, end_date) -> int:
        project = Project(name, description, start_date, end_date)
        return self.db_manager.add_project(project)

    def get_project(self, project_id) -> Project | None:
        return self.db_manager.get_project_by_id(project_id)

    def get_all_projects(self) -> list[Project]:
        return self.db_manager.get_all_projects()

    def update_project(self, project_id, **kwargs) -> bool:
        return self.db_manager.update_project(project_id, **kwargs)

    def delete_project(self, project_id) -> bool:
        return self.db_manager.delete_project(project_id)

    def update_project_status(self, project_id, new_status) -> bool:
        project = self.db_manager.get_project_by_id(project_id)
        if project is None:
            return False
        if not project.update_status(new_status):
            return False
        return self.db_manager.update_project(project_id, status=project.status)

    def get_project_progress(self, project_id) -> float:
        tasks = self.db_manager.get_tasks_by_project(project_id)
        if not tasks:
            return 0.0
        completed = len([task for task in tasks if task.status == "completed"])
        return round((completed / len(tasks)) * 100, 2)