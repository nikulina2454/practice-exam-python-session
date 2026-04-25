import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


class TaskView(ttk.Frame):
    def __init__(self, parent, task_controller, project_controller, user_controller) -> None:
        super().__init__(parent)
        self.task_controller = task_controller
        self.project_controller = project_controller
        self.user_controller = user_controller
        self.selected_task_id = None
        self.create_widgets()
        self.refresh_tasks()

    def create_widgets(self) -> None:
        form = ttk.Frame(self)
        form.pack(fill=tk.X, padx=10, pady=10)

        self.title_entry = ttk.Entry(form, width=22)
        self.title_entry.grid(row=0, column=0, padx=4)
        self.title_entry.insert(0, "Название")

        self.desc_entry = ttk.Entry(form, width=26)
        self.desc_entry.grid(row=0, column=1, padx=4)
        self.desc_entry.insert(0, "Описание")

        self.priority_cb = ttk.Combobox(form, width=8, values=[1, 2, 3], state="readonly")
        self.priority_cb.grid(row=0, column=2, padx=4)
        self.priority_cb.set("2")

        self.due_entry = ttk.Entry(form, width=12)
        self.due_entry.grid(row=0, column=3, padx=4)
        self.due_entry.insert(0, "YYYY-MM-DD")

        self.project_cb = ttk.Combobox(form, width=18, state="readonly")
        self.project_cb.grid(row=0, column=4, padx=4)

        self.user_cb = ttk.Combobox(form, width=18, state="readonly")
        self.user_cb.grid(row=0, column=5, padx=4)

        self.save_button = ttk.Button(form, text="Добавить", command=self.add_task)
        self.save_button.grid(row=0, column=6, padx=4)
        ttk.Button(form, text="Очистить", command=self._clear_form).grid(row=0, column=7, padx=4)
        ttk.Button(form, text="Удалить", command=self.delete_selected).grid(row=0, column=8, padx=4)

        tools_frame = ttk.Frame(self)
        tools_frame.pack(fill=tk.X, padx=10, pady=(0, 8))

        ttk.Label(tools_frame, text="Поиск:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(tools_frame, width=24)
        self.search_entry.pack(side=tk.LEFT, padx=(4, 12))

        ttk.Label(tools_frame, text="Статус:").pack(side=tk.LEFT)
        self.status_filter = ttk.Combobox(
            tools_frame,
            width=12,
            state="readonly",
            values=["all", "pending", "in_progress", "completed"],
        )
        self.status_filter.set("all")
        self.status_filter.pack(side=tk.LEFT, padx=(4, 12))

        ttk.Label(tools_frame, text="Приоритет:").pack(side=tk.LEFT)
        self.priority_filter = ttk.Combobox(
            tools_frame,
            width=8,
            state="readonly",
            values=["all", "1", "2", "3"],
        )
        self.priority_filter.set("all")
        self.priority_filter.pack(side=tk.LEFT, padx=(4, 12))

        ttk.Button(tools_frame, text="Применить", command=self.refresh_tasks).pack(side=tk.LEFT)
        ttk.Button(tools_frame, text="Сброс", command=self._reset_filters).pack(side=tk.LEFT, padx=(6, 0))

        self.tree = ttk.Treeview(
            self,
            columns=("id", "title", "priority", "status", "due_date", "project_id", "assignee_id"),
            show="headings",
        )
        for col, text, width in (
            ("id", "ID", 45),
            ("title", "Название", 210),
            ("priority", "Приоритет", 75),
            ("status", "Статус", 100),
            ("due_date", "Срок", 140),
            ("project_id", "Проект", 70),
            ("assignee_id", "Исполнитель", 90),
        ):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def refresh_tasks(self) -> None:
        projects = self.project_controller.get_all_projects()
        users = self.user_controller.get_all_users()
        self.project_map = {f"{project.id}: {project.name}": project.id for project in projects}
        self.user_map = {f"{user.id}: {user.username}": user.id for user in users}
        self.project_cb["values"] = list(self.project_map.keys())
        self.user_cb["values"] = list(self.user_map.keys())
        if self.project_cb["values"] and not self.project_cb.get():
            self.project_cb.current(0)
        if self.user_cb["values"] and not self.user_cb.get():
            self.user_cb.current(0)

        query = self.search_entry.get().strip()
        tasks = self.task_controller.search_tasks(query) if query else self.task_controller.get_all_tasks()
        if self.status_filter.get() != "all":
            tasks = [task for task in tasks if task.status == self.status_filter.get()]
        if self.priority_filter.get() != "all":
            tasks = [task for task in tasks if str(task.priority) == self.priority_filter.get()]

        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in tasks:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    task.id,
                    task.title,
                    task.priority,
                    task.status,
                    task.due_date.strftime("%Y-%m-%d"),
                    task.project_id,
                    task.assignee_id,
                ),
            )

    def add_task(self) -> None:
        try:
            if not self.project_cb.get() or not self.user_cb.get():
                raise ValueError("Сначала добавьте проект и пользователя")
            due_date = datetime.strptime(self.due_entry.get().strip(), "%Y-%m-%d")
            payload = {
                "title": self.title_entry.get().strip(),
                "description": self.desc_entry.get().strip(),
                "priority": int(self.priority_cb.get()),
                "due_date": due_date,
                "project_id": self.project_map[self.project_cb.get()],
                "assignee_id": self.user_map[self.user_cb.get()],
            }
            if self.selected_task_id is None:
                self.task_controller.add_task(
                    payload["title"],
                    payload["description"],
                    payload["priority"],
                    payload["due_date"],
                    payload["project_id"],
                    payload["assignee_id"],
                )
            else:
                self.task_controller.update_task(self.selected_task_id, **payload)
            self.refresh_tasks()
            self._clear_form()
        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        task_id = self.tree.item(selected[0])["values"][0]
        self.task_controller.delete_task(task_id)
        self.refresh_tasks()
        self._clear_form()

    def _on_select(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])["values"]
        self.selected_task_id = item[0]
        task = self.task_controller.get_task(self.selected_task_id)
        if task is None:
            return
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, task.title)
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, task.description)
        self.priority_cb.set(str(task.priority))
        self.due_entry.delete(0, tk.END)
        self.due_entry.insert(0, task.due_date.strftime("%Y-%m-%d"))
        for label, project_id in self.project_map.items():
            if project_id == task.project_id:
                self.project_cb.set(label)
                break
        for label, user_id in self.user_map.items():
            if user_id == task.assignee_id:
                self.user_cb.set(label)
                break
        self.save_button.config(text="Сохранить")

    def _clear_form(self):
        self.selected_task_id = None
        self.save_button.config(text="Добавить")
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.due_entry.insert(0, "YYYY-MM-DD")
        self.priority_cb.set("2")

    def _reset_filters(self):
        self.search_entry.delete(0, tk.END)
        self.status_filter.set("all")
        self.priority_filter.set("all")
        self.refresh_tasks()