from datetime import datetime

class Task:
    def __init__(self, title, description, priority, due_date, project_id, assignee_id) -> None:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title must be a non-empty string")
        if not isinstance(priority, int) or priority not in (1, 2, 3):
            raise ValueError("Priority must be 1, 2, or 3")
        if not isinstance(due_date, datetime):
            raise TypeError("Due date must be a datetime instance")
        if not isinstance(project_id, int) or project_id <= 0:
            raise ValueError("Project ID must be a positive integer")
        if not isinstance(assignee_id, int) or assignee_id <= 0:
            raise ValueError("Assignee ID must be a positive integer")

        self.id = None
        self.title = title.strip()
        self.description = description if description is not None else ""
        self.priority = priority
        self.status = "pending"
        self.due_date = due_date
        self.project_id = project_id
        self.assignee_id = assignee_id

    def update_status(self, new_status) -> bool:
        allowed_statuses = {"pending", "in_progress", "completed"}
        if new_status not in allowed_statuses:
            return False
        self.status = new_status
        return True

    def is_overdue(self) -> bool:
        return self.status != "completed" and self.due_date < datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date,
            "project_id": self.project_id,
            "assignee_id": self.assignee_id,
        }