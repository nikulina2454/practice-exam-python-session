import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


class ProjectView(ttk.Frame):
    def __init__(self, parent, project_controller) -> None:
        super().__init__(parent)
        self.project_controller = project_controller
        self.selected_project_id = None
        self.create_widgets()
        self.refresh_projects()

    def create_widgets(self) -> None:
        form = ttk.Frame(self)
        form.pack(fill=tk.X, padx=10, pady=10)

        self.name_entry = ttk.Entry(form, width=24)
        self.name_entry.grid(row=0, column=0, padx=4)
        self.name_entry.insert(0, "Название")

        self.desc_entry = ttk.Entry(form, width=28)
        self.desc_entry.grid(row=0, column=1, padx=4)
        self.desc_entry.insert(0, "Описание")

        self.start_entry = ttk.Entry(form, width=12)
        self.start_entry.grid(row=0, column=2, padx=4)
        self.start_entry.insert(0, "YYYY-MM-DD")

        self.end_entry = ttk.Entry(form, width=12)
        self.end_entry.grid(row=0, column=3, padx=4)
        self.end_entry.insert(0, "YYYY-MM-DD")

        self.status_cb = ttk.Combobox(
            form,
            width=12,
            state="readonly",
            values=["active", "completed", "on_hold"],
        )
        self.status_cb.set("active")
        self.status_cb.grid(row=0, column=4, padx=4)

        self.save_button = ttk.Button(form, text="Добавить", command=self.add_project)
        self.save_button.grid(row=0, column=5, padx=4)
        ttk.Button(form, text="Очистить", command=self._clear_form).grid(row=0, column=6, padx=4)
        ttk.Button(form, text="Удалить", command=self.delete_selected).grid(row=0, column=7, padx=4)

        body = ttk.Frame(self)
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        left = ttk.Frame(body)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right = ttk.Frame(body)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.tree = ttk.Treeview(
            left,
            columns=("id", "name", "status", "start_date", "end_date"),
            show="headings",
        )
        for col, text, width in (
            ("id", "ID", 45),
            ("name", "Название", 180),
            ("status", "Статус", 90),
            ("start_date", "Начало", 120),
            ("end_date", "Окончание", 120),
        ):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        ttk.Label(right, text="Задачи проекта").pack(anchor=tk.W)
        self.tasks_tree = ttk.Treeview(
            right,
            columns=("id", "title", "status", "priority"),
            show="headings",
            height=12,
        )
        for col, text, width in (
            ("id", "ID", 45),
            ("title", "Название", 180),
            ("status", "Статус", 95),
            ("priority", "Приоритет", 75),
        ):
            self.tasks_tree.heading(col, text=text)
            self.tasks_tree.column(col, width=width, anchor=tk.CENTER)
        self.tasks_tree.pack(fill=tk.BOTH, expand=True, pady=(4, 8))

        self.progress_label = ttk.Label(right, text="Прогресс: 0.00%")
        self.progress_label.pack(anchor=tk.W)

    def refresh_projects(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for project in self.project_controller.get_all_projects():
            self.tree.insert(
                "",
                tk.END,
                values=(
                    project.id,
                    project.name,
                    project.status,
                    project.start_date.strftime("%Y-%m-%d"),
                    project.end_date.strftime("%Y-%m-%d"),
                ),
            )
        self._refresh_project_tasks()

    def add_project(self) -> None:
        try:
            start_date = datetime.strptime(self.start_entry.get().strip(), "%Y-%m-%d")
            end_date = datetime.strptime(self.end_entry.get().strip(), "%Y-%m-%d")
            if self.selected_project_id is None:
                project_id = self.project_controller.add_project(
                    self.name_entry.get().strip(),
                    self.desc_entry.get().strip(),
                    start_date,
                    end_date,
                )
                self.project_controller.update_project_status(project_id, self.status_cb.get())
            else:
                self.project_controller.update_project(
                    self.selected_project_id,
                    name=self.name_entry.get().strip(),
                    description=self.desc_entry.get().strip(),
                    start_date=start_date,
                    end_date=end_date,
                    status=self.status_cb.get(),
                )
            self.refresh_projects()
            self._clear_form()
        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        project_id = self.tree.item(selected[0])["values"][0]
        self.project_controller.delete_project(project_id)
        self.refresh_projects()
        self._clear_form()

    def _on_select(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return
        project_id = self.tree.item(selected[0])["values"][0]
        project = self.project_controller.get_project(project_id)
        if project is None:
            return
        self.selected_project_id = project.id
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, project.name)
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, project.description)
        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, project.start_date.strftime("%Y-%m-%d"))
        self.end_entry.delete(0, tk.END)
        self.end_entry.insert(0, project.end_date.strftime("%Y-%m-%d"))
        self.status_cb.set(project.status)
        self.save_button.config(text="Сохранить")
        self._refresh_project_tasks()

    def _refresh_project_tasks(self):
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        if self.selected_project_id is None:
            self.progress_label.config(text="Прогресс: 0.00%")
            return
        tasks = self.project_controller.db_manager.get_tasks_by_project(self.selected_project_id)
        for task in tasks:
            self.tasks_tree.insert(
                "",
                tk.END,
                values=(task.id, task.title, task.status, task.priority),
            )
        progress = self.project_controller.get_project_progress(self.selected_project_id)
        self.progress_label.config(text=f"Прогресс: {progress:.2f}%")

    def _clear_form(self):
        self.selected_project_id = None
        self.save_button.config(text="Добавить")
        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.start_entry.insert(0, "YYYY-MM-DD")
        self.end_entry.insert(0, "YYYY-MM-DD")
        self.status_cb.set("active")
        self._refresh_project_tasks()