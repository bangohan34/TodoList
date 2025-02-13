import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime

class TodoApp:
    # 初期化
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.tasks = [] # タスクを保持するためのリストを初期化

        # ウィンドウ表示
        self.show_tasks_window()

    # タスク追加画面
    def add_task_window(self):
        task_window=tk.Toplevel(self.root)
        task_window.title("タスク追加")

        # 重要度
        self.priority_label = ttk.Label(task_window, text="重要度:")
        self.priority_label.grid(row=0, column=0, pady=5)
        self.priority_combobox = ttk.Combobox(task_window, values=["！超重要！", "重要", "なるはや", "いつでも"])
        self.priority_combobox.grid(row=0, column=1, pady=5)

        # 内容
        self.content_label = ttk.Label(task_window, text="内容:")
        self.content_label.grid(row=1, column=0, pady=5)
        self.content_entry = ttk.Entry(task_window)
        self.content_entry.grid(row=1, column=1, pady=5)

        # 締切
        self.deadline_label = ttk.Label(task_window, text="締切:")
        self.deadline_label.grid(row=2, column=0, pady=5)
        self.deadline_entry = DateEntry(task_window, date_pattern='yyyy/mm/dd')
        self.deadline_entry.grid(row=2, column=1, pady=5)

        # タスクの種類
        self.type_label = ttk.Label(task_window, text="タスクの種類:")
        self.type_label.grid(row=3, column=0, pady=5)
        self.type_combobox = ttk.Combobox(task_window, values=["就活", "研究", "講義", "その他"])
        self.type_combobox.grid(row=3, column=1, pady=5)

        # タスク追加のボタン
        self.add_button = ttk.Button(task_window, text="タスクを追加する", command=self.update_task_window)
        self.add_button.grid(row=4, columnspan=2, pady=10)

    #タスクの削除
    def delete_task(self):
        selected_items = self.task_tree.selection()
        if not selected_items:
            messagebox.showwarning("選択エラー", "削除するタスクを選択してください")
            return
        for selected_item in selected_items:
            task_index = int(self.task_tree.item(selected_item, "tags")[0].split("_")[1])
            del self.tasks[task_index]
        self.display_tasks()


    # タスク追加を押すと、タスク一覧を更新
    def update_task_window(self):
        self.add_task()
        self.display_tasks()
    
    # タスク検索機能
    def search_tasks(self):
        search_text = self.search_entry.get().lower()
        matching_tasks = [task for task in self.tasks if search_text in task["content"].lower() or search_text in task["type"].lower()]
        for row in self.task_tree.get_children():
            self.task_tree.delete(row)
        for index, task in enumerate(matching_tasks):
            tag_name = f"task_{index}"
            self.task_tree.tag_configure(tag_name, background=task["color"])
            self.task_tree.insert("", tk.END, values=(task["priority"], task["content"], task["deadline"], task["type"]), tags=(tag_name,))


    # タスク追加の詳細情報
    def add_task(self):
        priority = self.priority_combobox.get()
        content = self.content_entry.get()
        deadline = self.deadline_entry.get()
        task_type = self.type_combobox.get()
        color_map = {"就活": "violet", "研究": "lightskyblue", "講義": "lightgreen", "その他": "lightyellow"}
        color = color_map.get(task_type, "white")

        # 全ての項目が埋まっているかどうか
        if priority and content and deadline and task_type:
            self.tasks.append({"priority": priority, "content": content, "deadline": deadline, "type": task_type, "color": color})
            self.priority_combobox.set("")
            self.content_entry.delete(0, tk.END)
            self.deadline_entry.set_date(datetime.date.today())
            self.type_combobox.set("")
        else:
            messagebox.showwarning("入力エラー", "全ての項目を入力してください")

    # タスク一覧表示
    def show_tasks_window(self):

        # 検索バーの追加
        search_frame = ttk.Frame(self.root)
        search_frame.pack(padx=10, pady=10, fill=tk.X)

        search_label = ttk.Label(search_frame, text="検索:")
        search_label.pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        search_button = ttk.Button(search_frame, text="検索", command=self.search_tasks)
        search_button.pack(side=tk.LEFT, padx=5)

        tree = ttk.Treeview(self.root, columns=("priority", "content", "deadline", "type"), show="headings")
        tree.heading("priority", text="重要度")
        tree.heading("content", text="内容")
        tree.heading("deadline", text="締切")
        tree.heading("type", text="タスクの種類")

        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # タスクを表示する
        for index, task in enumerate(self.tasks):
            tag_name = f"task_{index}"
            tree.tag_configure(tag_name, background=task["color"])
            tree.insert("", tk.END, values=(task["priority"], task["content"], task["deadline"], task["type"]), tags=(tag_name,))

        # 並べ替え機能の追加
        sort_frame = ttk.Frame(self.root)
        sort_frame.pack(padx=10, pady=10, fill=tk.X)

        sort_label = ttk.Label(sort_frame, text="並べ替え:")
        sort_label.pack(side=tk.LEFT, padx=5)
        self.sort_combobox = ttk.Combobox(sort_frame, values=["重要度", "タスクの種類", "締切"])
        self.sort_combobox.pack(side=tk.LEFT, padx=5)
        sort_button = ttk.Button(sort_frame, text="並べ替え", command=self.sort_tasks)
        sort_button.pack(side=tk.LEFT, padx=5)

        self.task_tree = tree

        # タスク追加画面表示
        self.add_task_window_button = ttk.Button(self.root, text="タスクを追加", command=self.add_task_window)
        self.add_task_window_button.pack(pady=10)

        # タスク削除ボタン
        self.delete_task_button = ttk.Button(self.root, text="タスクを削除", command=self.delete_task)
        self.delete_task_button.pack(side=tk.LEFT, pady=10)


    # タスク一覧更新
    def display_tasks(self):
        for row in self.task_tree.get_children():
            self.task_tree.delete(row)
        for index, task in enumerate(self.tasks):
            tag_name = f"task_{index}"
            self.task_tree.tag_configure(tag_name, background=task["color"])
            self.task_tree.insert("", tk.END, values=(task["priority"], task["content"], task["deadline"], task["type"], task["color"]), tags=(tag_name,))

    # タスクの並び替え
    def sort_tasks(self):
        sort_key_map = {"重要度": "priority", "タスクの種類": "type", "締切": "deadline"}
        sort_key = sort_key_map.get(self.sort_combobox.get())
        if sort_key:
            if sort_key == "priority":
                self.tasks.sort(key=lambda x: x[sort_key], reverse=True)
            else:
                self.tasks.sort(key=lambda x: x[sort_key])
            self.display_tasks()
        else:
            messagebox.showwarning("並べ替えエラー", "無効な並べ替えキーです")


# アプリを実行
if __name__ == "__main__":
    root = tk.Tk() # ディスプレイを表示
    app = TodoApp(root) # アプリの初期化・立ち上げ
    root.mainloop()