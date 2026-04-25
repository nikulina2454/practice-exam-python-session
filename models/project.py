from datetime import datetime

class Project:
    def __init__(self, name, description, start_date, end_date) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Project name must be a non-empty string")
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise TypeError("Start date and end date must be datetime instances")
        if end_date < start_date:
            raise ValueError("End date cannot be earlier than start date")

        self.id = None
        self.name = name.strip()
        self.description = description if description is not None else ""
        self.start_date = start_date
        self.end_date = end_date
        self.status = "active"

    def update_status(self, new_status) -> bool:
        allowed_statuses = {"active", "completed", "on_hold"}
        if new_status not in allowed_statuses:
            return False
        self.status = new_status
        return True

    def get_progress(self) -> float:
        now = datetime.now()
        if now <= self.start_date:
            return 0.0
        if now >= self.end_date:
            return 100.0
        total_seconds = (self.end_date - self.start_date).total_seconds()
        if total_seconds <= 0:
            return 100.0
        elapsed_seconds = (now - self.start_date).total_seconds()
        return round((elapsed_seconds / total_seconds) * 100, 2)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
        }