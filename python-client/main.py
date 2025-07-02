import requests
import tkinter as tk
from tkinter import messagebox, simpledialog

BASE_URL = "http://localhost:8080/todos"

root = tk.Tk()
root.title("ToDoアプリ")
root.minsize(width=400, height=300)

filter_var = tk.StringVar(value="all")
filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

tk.Radiobutton(filter_frame, text="全て", variable=filter_var, value="all", command=lambda: fetch_tasks()).pack(side="left")
tk.Radiobutton(filter_frame, text="完了済み", variable=filter_var, value="done", command=lambda: fetch_tasks()).pack(side="left")
tk.Radiobutton(filter_frame, text="未完了", variable=filter_var, value="undone", command=lambda: fetch_tasks()).pack(side="left")

task_frame = tk.Frame(root)
task_frame.pack(pady=10)

def add_task(event=None):
    task = task_entry.get()
    if not task.strip():
        messagebox.showwarning("警告", "タスクを入力してください")
        return
    if api_request("post", data={"task": task, "done": False}):
        task_entry.delete(0, tk.END)
        fetch_tasks()

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
        tasks.sort(key=lambda x: x["done"])  # 未完了→完了の順に並べる
        update_task_list(tasks)

def delete_task(task_id):
    if messagebox.askyesno("確認", "このタスクを削除しますか？"):
        if api_request("delete", f"/{task_id}"):
            messagebox.showinfo("削除完了", "タスクを削除しました。")
            fetch_tasks()
        else:
            messagebox.showerror("エラー", "削除に失敗しました")

def toggle_done(task_id, task_text, var):
    new_done = var.get()
    data = {"id": task_id, "task": task_text, "done": new_done}
    if not api_request("put", f"/{task_id}", data):
        messagebox.showerror("エラー", "状態の更新に失敗しました")
    fetch_tasks() 

def edit_task(task_id, old_task, done_status):
    new_task = simpledialog.askstring("編集", "新しいタスク名を入力：", initialvalue=old_task, parent=root)
    if new_task and new_task.strip() and new_task != old_task:
        data = {"id": task_id, "task": new_task, "done": done_status}
        if not api_request("put", f"/{task_id}", data):
            messagebox.showerror("エラー", "編集に失敗しました")
        fetch_tasks()

def update_task_list(tasks):
    for widget in task_frame.winfo_children():
        widget.destroy()

    for task in tasks:
        var = tk.BooleanVar(value=task["done"])
        row_frame = tk.Frame(task_frame)
        row_frame.pack(fill="x", pady=2)

        fg_color = "gray" if task["done"] else "black"
        font_style = ("Arial", 10, "overstrike") if task["done"] else ("Arial", 10)

        chk = tk.Checkbutton(
            row_frame,
            text=task["task"],
            variable=var,
            command=lambda tid=task["id"], t=task["task"], v=var: toggle_done(tid, t, v),
            fg=fg_color,
            font=font_style,
            anchor="w",
            width=25
        )
        chk.grid(row=0, column=0, sticky="w")

        status_text = "完了" if task["done"] else "未完了"
        status_label = tk.Label(row_frame, text=status_text, width=6, anchor="center", fg=fg_color)
        status_label.grid(row=0, column=1, padx=5)

        edit_btn = tk.Button(
            row_frame,
            text="編集",
            width=6,
            command=lambda tid=task["id"], t=task["task"], d=task["done"]: edit_task(tid, t, d)
        )
        edit_btn.grid(row=0, column=2, padx=3)

        del_btn = tk.Button(
            row_frame,
            text="削除",
            width=6,
            command=lambda tid=task["id"]: delete_task(tid)
        )
        del_btn.grid(row=0, column=3, padx=3)

input_frame = tk.Frame(root)
input_frame.pack(pady=5)

task_entry = tk.Entry(input_frame, width=30)
task_entry.pack(side="left", padx=5)

add_button = tk.Button(input_frame, text="追加", command=add_task)
add_button.pack(side="left")

task_entry.bind("<Return>", add_task)

fetch_tasks()
root.mainloop()




