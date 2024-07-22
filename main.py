import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime

class TodoApp:
    # 初期化
    def __init__(self, root):
        self.root = root
        self.root.title("ますとマン")
        self.tasks = [{"priority": "重要", "content": "プレゼン資料作成", "deadline": "2024/07/31", "type": "研究", "color": "lightskyblue"},
            {"priority": "！超重要！", "content": "就職活動", "deadline": "2024/08/15", "type": "就活", "color": "violet"},
            {"priority": "なるはや", "content": "講義の復習", "deadline": "2024/08/01", "type": "講義", "color": "lightgreen"},
            {"priority": "いつでも", "content": "読書", "deadline": "2024/09/01", "type": "その他", "color": "lightyellow"}
        ]
        self.sort_order = {"priority": False, "content": False, "deadline": False, "type": False}

        # ウィンドウ表示
        self.show_tasks_window()

    # タスク一覧表示
    def show_tasks_window(self):
        tree = ttk.Treeview(self.root, columns=("priority", "content", "deadline", "type"), show="headings")
        tree.heading("priority", text="重要度", command=lambda: self.sort_by_column("priority"))
        tree.heading("content", text="内容", command=lambda: self.sort_by_column("content"))
        tree.heading("deadline", text="締切", command=lambda: self.sort_by_column("deadline"))
        tree.heading("type", text="タスクの種類", command=lambda: self.sort_by_column("type"))

        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # タスクを表示する
        for index, task in enumerate(self.tasks):
            tag_name = f"task_{index}"
            tree.tag_configure(tag_name, background=task["color"])
            tree.insert("", tk.END, values=(task["priority"], task["content"], task["deadline"], task["type"]), tags=(tag_name,))
        
        # ダブルクリックで編集
        tree.bind("<Double-1>", self.on_task_double_click)

        # 並べ替え機能の追加
        self.task_tree = tree

        # タスク削除ボタン表示
        self.delete_task_button = ttk.Button(self.root, text="タスクを削除", command=self.delete_task)
        self.delete_task_button.pack(side=tk.RIGHT, pady=10)

        # タスク追加ボタン表示
        self.add_task_window_button = ttk.Button(self.root, text="タスクを追加", command=self.add_task_window)
        self.add_task_window_button.pack(pady=10)

    # 並び替え
    def sort_by_column(self, column):
        self.sort_order[column] = not self.sort_order[column]
        reverse = self.sort_order[column]
        self.tasks.sort(key=lambda x: x[column], reverse=reverse)
        self.display_tasks()

    # ダブルクリック
    def on_task_double_click(self, event):
        item = self.task_tree.selection()[0]
        index=self.task_tree.index(item)
        self.edit_task_window(index)

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
    
    # タスク追加を押すと、タスク一覧を更新
    def update_task_window(self):
        self.add_task()
        self.display_tasks()
    
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

    # タスク編集画面
    def edit_task_window(self,index):
        task=self.tasks[index]
        self.task_window=tk.Toplevel(self.root)
        self.task_window.title("タスク編集")

        self.priority_label = ttk.Label(self.task_window, text="重要度:")
        self.priority_label.grid(row=0, column=0, pady=5)
        self.priority_combobox = ttk.Combobox(self.task_window, values=["！超重要！", "重要", "なるはや", "いつでも"])
        self.priority_combobox.set(task["priority"])
        self.priority_combobox.grid(row=0, column=1, pady=5)

        self.content_label = ttk.Label(self.task_window, text="内容:")
        self.content_label.grid(row=1, column=0, pady=5)
        self.content_entry = ttk.Entry(self.task_window)
        self.content_entry.insert(0, task["content"])
        self.content_entry.grid(row=1, column=1, pady=5)

        self.deadline_label = ttk.Label(self.task_window, text="締切:")
        self.deadline_label.grid(row=2, column=0, pady=5)
        self.deadline_entry = DateEntry(self.task_window, date_pattern='yyyy/mm/dd')
        self.deadline_entry.set_date(task["deadline"])
        self.deadline_entry.grid(row=2, column=1, pady=5)

        self.type_label = ttk.Label(self.task_window, text="タスクの種類:")
        self.type_label.grid(row=3, column=0, pady=5)
        self.type_combobox = ttk.Combobox(self.task_window, values=["就活", "研究", "講義", "その他"])
        self.type_combobox.set(task["type"])
        self.type_combobox.grid(row=3, column=1, pady=5)

        self.update_button = ttk.Button(self.task_window, text="タスクを更新する", command=lambda: self.update_task(index))
        self.update_button.grid(row=4, columnspan=2, pady=10)

    # タスク編集して更新
    def update_task(self, index):
        priority = self.priority_combobox.get()
        content = self.content_entry.get()
        deadline = self.deadline_entry.get()
        task_type = self.type_combobox.get()
        color_map = {"就活": "violet", "研究": "lightskyblue", "講義": "lightgreen", "その他": "lightyellow"}
        color = color_map.get(task_type, "white")

        if priority and content and deadline and task_type:
            self.tasks[index] = {"priority": priority, "content": content, "deadline": deadline, "type": task_type, "color": color}
            self.display_tasks()
            self.task_window.destroy()
        else:
            messagebox.showwarning("入力エラー", "全ての項目を入力してください")

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

    # タスク一覧更新
    def display_tasks(self):
        for row in self.task_tree.get_children():
            self.task_tree.delete(row)
        for index, task in enumerate(self.tasks):
            tag_name = f"task_{index}"
            self.task_tree.tag_configure(tag_name, background=task["color"])
            self.task_tree.insert("", tk.END, values=(task["priority"], task["content"], task["deadline"], task["type"], task["color"]), tags=(tag_name,))

# アプリを実行
if __name__ == "__main__":
    root = tk.Tk() # ディスプレイを表示
    app = TodoApp(root) # アプリの初期化・立ち上げ
    root.mainloop()
