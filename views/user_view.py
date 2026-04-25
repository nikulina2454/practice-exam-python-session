import tkinter as tk
from tkinter import messagebox, ttk


class UserView(ttk.Frame):
    def __init__(self, parent, user_controller) -> None:
        super().__init__(parent)
        self.user_controller = user_controller
        self.selected_user_id = None
        self.create_widgets()
        self.refresh_users()

    def create_widgets(self) -> None:
        form = ttk.Frame(self)
        form.pack(fill=tk.X, padx=10, pady=10)

        self.username_entry = ttk.Entry(form, width=24)
        self.username_entry.grid(row=0, column=0, padx=4)
        self.username_entry.insert(0, "Username")

        self.email_entry = ttk.Entry(form, width=30)
        self.email_entry.grid(row=0, column=1, padx=4)
        self.email_entry.insert(0, "Email")

        self.role_cb = ttk.Combobox(
            form,
            width=12,
            values=["admin", "manager", "developer"],
            state="readonly",
        )
        self.role_cb.grid(row=0, column=2, padx=4)
        self.role_cb.set("developer")

        self.save_button = ttk.Button(form, text="Добавить", command=self.add_user)
        self.save_button.grid(row=0, column=3, padx=4)
        ttk.Button(form, text="Очистить", command=self._clear_form).grid(row=0, column=4, padx=4)
        ttk.Button(form, text="Удалить", command=self.delete_selected).grid(row=0, column=5, padx=4)

        body = ttk.Frame(self)
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        left = ttk.Frame(body)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right = ttk.Frame(body)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.tree = ttk.Treeview(
            left,
            columns=("id", "username", "email", "role"),
            show="headings",
        )
        for col, text, width in (
            ("id", "ID", 45),
            ("username", "Username", 160),
            ("email", "Email", 230),
            ("role", "Role", 90),
        ):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        ttk.Label(right, text="Задачи пользователя").pack(anchor=tk.W)
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
        self.tasks_tree.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

    def refresh_users(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for user in self.user_controller.get_all_users():
            self.tree.insert("", tk.END, values=(user.id, user.username, user.email, user.role))
        self._refresh_user_tasks()

    def add_user(self) -> None:
        try:
            if self.selected_user_id is None:
                self.user_controller.add_user(
                    self.username_entry.get().strip(),
                    self.email_entry.get().strip(),
                    self.role_cb.get(),
                )
            else:
                self.user_controller.update_user(
                    self.selected_user_id,
                    username=self.username_entry.get().strip(),
                    email=self.email_entry.get().strip(),
                    role=self.role_cb.get(),
                )
            self.refresh_users()
            self._clear_form()
        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    def delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        user_id = self.tree.item(selected[0])["values"][0]
        self.user_controller.delete_user(user_id)
        self.refresh_users()
        self._clear_form()

    def _on_select(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])["values"]
        self.selected_user_id = item[0]
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, item[1])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, item[2])
        self.role_cb.set(item[3])
        self.save_button.config(text="Сохранить")
        self._refresh_user_tasks()

    def _refresh_user_tasks(self):
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        if self.selected_user_id is None:
            return
        for task in self.user_controller.get_user_tasks(self.selected_user_id):
            self.tasks_tree.insert(
                "",
                tk.END,
                values=(task.id, task.title, task.status, task.priority),
            )

    def _clear_form(self):
        self.selected_user_id = None
        self.save_button.config(text="Добавить")
        self.username_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.role_cb.set("developer")
        self._refresh_user_tasks()