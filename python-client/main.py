import requests
import tkinter as tk
from tkinter import messagebox

BASE_URL = "http://localhost:8080/todos"

root = tk.Tk()
root.title("ToDoアプリ")

task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=5)

filter_var = tk.StringVar(value="all")  # フィルター状態

filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

tk.Radiobutton(filter_frame, text="全て", variable=filter_var, value="all", command=lambda: fetch_tasks()).pack(side="left")
tk.Radiobutton(filter_frame, text="完了済み", variable=filter_var, value="done", command=lambda: fetch_tasks()).pack(side="left")
tk.Radiobutton(filter_frame, text="未完了", variable=filter_var, value="undone", command=lambda: fetch_tasks()).pack(side="left")

task_frame = tk.Frame(root)
task_frame.pack(pady=10)

def api_request(method, path="", data=None):
    try:
        response = requests.request(method, f"{BASE_URL}{path}", json=data)
        response.raise_for_status()
        if response.status_code != 204:
            return response.json()
    except requests.RequestException as e:
        messagebox.showerror("通信エラー", str(e))
    return None

def fetch_tasks():
    tasks = api_request("get")
    if tasks is not None:
        filter_val = filter_var.get()
        if filter_val == "done":
            tasks = [t for t in tasks if t["done"]]
        elif filter_val == "undone":
            tasks = [t for t in tasks if not t["done"]]
        update_task_list(tasks)

def add_task():
    task = task_entry.get()
    if not task.strip():
        messagebox.showwarning("警告", "タスクを入力してください")
        return
    if api_request("post", data={"task": task, "done": False}):
        task_entry.delete(0, tk.END)
        fetch_tasks()

def delete_task(task_id):
    if api_request("delete", f"/{task_id}"):
        fetch_tasks()
    else:
        messagebox.showerror("エラー", "削除に失敗しました")

def toggle_done(task_id, task_text, var):
    new_done = var.get()
    data = {"id": task_id, "task": task_text, "done": new_done}
    if not api_request("put", f"/{task_id}", data):
        messagebox.showerror("エラー", "状態の更新に失敗しました")
        fetch_tasks()

def update_task_list(tasks):
    for widget in task_frame.winfo_children():
        widget.destroy()

    for task in tasks:
        var = tk.BooleanVar(value=task["done"])

        row_frame = tk.Frame(task_frame)
        row_frame.pack(fill="x", pady=2)

        chk = tk.Checkbutton(
            row_frame,
            text=task["task"],
            variable=var,
            command=lambda tid=task["id"], t=task["task"], v=var: toggle_done(tid, t, v)
        )
        chk.pack(side="left", anchor="w")

        btn = tk.Button(
            row_frame,
            text="削除",
            command=lambda tid=task["id"]: delete_task(tid)
        )
        btn.pack(side="left", padx=10)

        tk.Frame(task_frame, height=2).pack()

add_button = tk.Button(root, text="追加", command=add_task)
add_button.pack(pady=5)

fetch_tasks()
root.mainloop()



