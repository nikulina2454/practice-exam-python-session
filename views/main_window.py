# Главное окно приложения согласно README.md

import tkinter as tk
from tkinter import ttk
from views.project_view import ProjectView
from views.task_view import TaskView
from views.user_view import UserView

class MainWindow(tk.Tk):
    def __init__(self, task_controller, project_controller, user_controller) -> None:
        super().__init__()
        self.title("Система управления задачами")
        self.geometry("980x640")
        self.task_controller = task_controller
        self.project_controller = project_controller
        self.user_controller = user_controller

        menu_bar = tk.Menu(self)
        app_menu = tk.Menu(menu_bar, tearoff=0)
        app_menu.add_command(label="Обновить данные", command=self._refresh_all_views)
        app_menu.add_separator()
        app_menu.add_command(label="Выход", command=self.destroy)
        menu_bar.add_cascade(label="Приложение", menu=app_menu)
        self.config(menu=menu_bar)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.task_view = TaskView(notebook, task_controller, project_controller, user_controller)
        self.project_view = ProjectView(notebook, project_controller)
        self.user_view = UserView(notebook, user_controller)

        notebook.add(self.task_view, text="Задачи")
        notebook.add(self.project_view, text="Проекты")
        notebook.add(self.user_view, text="Пользователи")

    def _refresh_all_views(self):
        self.project_view.refresh_projects()
        self.user_view.refresh_users()
        self.task_view.refresh_tasks()

