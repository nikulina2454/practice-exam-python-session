import sqlite3
from datetime import datetime
from models.project import Project
from models.task import Task
from models.user import User

class DatabaseManager:
    def __init__(self, db_path="tasks.db") -> None:
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        self.connection.close()

    def create_tables(self) -> None:
        self.create_project_table()
        self.create_user_table()
        self.create_task_table()

    def create_task_table(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                priority INTEGER NOT NULL,
                status TEXT NOT NULL,
                due_date TEXT NOT NULL,
                project_id INTEGER NOT NULL,
                assignee_id INTEGER NOT NULL,
                FOREIGN KEY(project_id) REFERENCES projects(id),
                FOREIGN KEY(assignee_id) REFERENCES users(id)
            )
            """
        )
        self.connection.commit()

    def create_project_table(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def create_user_table(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                registration_date TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def _task_from_row(self, row) -> Task:
        task = Task(
            title=row["title"],
            description=row["description"],
            priority=row["priority"],
            due_date=datetime.fromisoformat(row["due_date"]),
            project_id=row["project_id"],
            assignee_id=row["assignee_id"],
        )
        task.id = row["id"]
        task.status = row["status"]
        return task

    def _project_from_row(self, row) -> Project:
        project = Project(
            name=row["name"],
            description=row["description"],
            start_date=datetime.fromisoformat(row["start_date"]),
            end_date=datetime.fromisoformat(row["end_date"]),
        )
        project.id = row["id"]
        project.status = row["status"]
        return project

    def _user_from_row(self, row) -> User:
        user = User(username=row["username"], email=row["email"], role=row["role"])
        user.id = row["id"]
        user.registration_date = datetime.fromisoformat(row["registration_date"])
        return user

    def add_task(self, task: Task) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO tasks (title, description, priority, status, due_date, project_id, assignee_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task.title,
                task.description,
                task.priority,
                task.status,
                task.due_date.isoformat(),
                task.project_id,
                task.assignee_id,
            ),
        )
        self.connection.commit()
        return cursor.lastrowid

    def get_task_by_id(self, task_id) -> Task | None:
        cursor = self.connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._task_from_row(row)

    def get_all_tasks(self) -> list[Task]:
        cursor = self.connection.execute("SELECT * FROM tasks")
        return [self._task_from_row(row) for row in cursor.fetchall()]

    def update_task(self, task_id, **kwargs) -> bool:
        allowed_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "project_id",
            "assignee_id",
        }
        updates = []
        values = []
        for key, value in kwargs.items():
            if key not in allowed_fields:
                continue
            if key == "due_date" and isinstance(value, datetime):
                value = value.isoformat()
            updates.append(f"{key} = ?")
            values.append(value)

        if not updates:
            return False

        values.append(task_id)
        cursor = self.connection.execute(
            f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?",
            tuple(values),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def delete_task(self, task_id) -> bool:
        cursor = self.connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.connection.commit()
        return cursor.rowcount > 0

    def search_tasks(self, query) -> list[Task]:
        pattern = f"%{query}%"
        cursor = self.connection.execute(
            "SELECT * FROM tasks WHERE title LIKE ? OR description LIKE ?",
            (pattern, pattern),
        )
        return [self._task_from_row(row) for row in cursor.fetchall()]

    def get_tasks_by_project(self, project_id) -> list[Task]:
        cursor = self.connection.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,))
        return [self._task_from_row(row) for row in cursor.fetchall()]

    def get_tasks_by_user(self, user_id) -> list[Task]:
        cursor = self.connection.execute("SELECT * FROM tasks WHERE assignee_id = ?", (user_id,))
        return [self._task_from_row(row) for row in cursor.fetchall()]

    def add_project(self, project: Project) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO projects (name, description, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                project.name,
                project.description,
                project.start_date.isoformat(),
                project.end_date.isoformat(),
                project.status,
            ),
        )
        self.connection.commit()
        return cursor.lastrowid

    def get_project_by_id(self, project_id) -> Project | None:
        cursor = self.connection.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._project_from_row(row)

    def get_all_projects(self) -> list[Project]:
        cursor = self.connection.execute("SELECT * FROM projects")
        return [self._project_from_row(row) for row in cursor.fetchall()]

    def update_project(self, project_id, **kwargs) -> bool:
        allowed_fields = {"name", "description", "start_date", "end_date", "status"}
        updates = []
        values = []
        for key, value in kwargs.items():
            if key not in allowed_fields:
                continue
            if key in {"start_date", "end_date"} and isinstance(value, datetime):
                value = value.isoformat()
            updates.append(f"{key} = ?")
            values.append(value)

        if not updates:
            return False

        values.append(project_id)
        cursor = self.connection.execute(
            f"UPDATE projects SET {', '.join(updates)} WHERE id = ?",
            tuple(values),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def delete_project(self, project_id) -> bool:
        cursor = self.connection.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        self.connection.commit()
        return cursor.rowcount > 0

    def add_user(self, user: User) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO users (username, email, role, registration_date)
            VALUES (?, ?, ?, ?)
            """,
            (
                user.username,
                user.email,
                user.role,
                user.registration_date.isoformat(),
            ),
        )
        self.connection.commit()
        return cursor.lastrowid

    def get_user_by_id(self, user_id) -> User | None:
        cursor = self.connection.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._user_from_row(row)

    def get_all_users(self) -> list[User]:
        cursor = self.connection.execute("SELECT * FROM users")
        return [self._user_from_row(row) for row in cursor.fetchall()]

    def update_user(self, user_id, **kwargs) -> bool:
        allowed_fields = {"username", "email", "role", "registration_date"}
        updates = []
        values = []
        for key, value in kwargs.items():
            if key not in allowed_fields:
                continue
            if key == "registration_date" and isinstance(value, datetime):
                value = value.isoformat()
            updates.append(f"{key} = ?")
            values.append(value)

        if not updates:
            return False

        values.append(user_id)
        cursor = self.connection.execute(
            f"UPDATE users SET {', '.join(updates)} WHERE id = ?",
            tuple(values),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def delete_user(self, user_id) -> bool:
        cursor = self.connection.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.connection.commit()
        return cursor.rowcount > 0