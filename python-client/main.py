import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import json
import os
from datetime import datetime

BASE_URL = "http://localhost:8080/todos"
LOCAL_FILE = "todos.json"

root = tk.Tk()
root.title("ToDoアプリ")
root.geometry("850x600")
root.minsize(800, 500)

filter_var = tk.StringVar(value="all")
filter_tag = tk.StringVar()
filter_date = tk.StringVar()
sort_order = tk.StringVar(value="none")

# 入力欄用変数
task_input = tk.StringVar()
date_input = tk.StringVar()
tags_input = tk.StringVar()

# 入力欄
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="タスク").grid(row=0, column=0)
tk.Entry(input_frame, textvariable=task_input, width=25).grid(row=0, column=1)

tk.Label(input_frame, text="期限 (YYYYMMDD)").grid(row=0, column=2)
date_entry = tk.Entry(input_frame, textvariable=date_input, width=15)
date_entry.grid(row=0, column=3)

tk.Label(input_frame, text="タグ（, 区切り）").grid(row=0, column=4)
tk.Entry(input_frame, textvariable=tags_input, width=20).grid(row=0, column=5)

tk.Button(input_frame, text="追加", command=lambda: add_task()).grid(row=0, column=6, padx=5)

def force_half_width(event):
    val = date_input.get()
    new_val = val.translate(str.maketrans({
        '０': '0', '１': '1', '２': '2', '３': '3', '４': '4',
        '５': '5', '６': '6', '７': '7', '８': '8', '９': '9'
    }))
    date_input.set(new_val)
date_entry.bind("<KeyRelease>", force_half_width)

# フィルター
filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="表示：").pack(side="left")
tk.Radiobutton(filter_frame, text="全て", variable=filter_var, value="all", command=lambda: fetch_tasks()).pack(side="left")
tk.Radiobutton(filter_frame, text="完了", variable=filter_var, value="done", command=lambda: fetch_tasks()).pack(side="left")
tk.Radiobutton(filter_frame, text="未完了", variable=filter_var, value="undone", command=lambda: fetch_tasks()).pack(side="left")

tk.Label(filter_frame, text="　タグ:").pack(side="left")
tk.Entry(filter_frame, textvariable=filter_tag, width=10).pack(side="left")

tk.Label(filter_frame, text="日付:").pack(side="left")
tk.Entry(filter_frame, textvariable=filter_date, width=10).pack(side="left")

tk.Button(filter_frame, text="適用", command=lambda: fetch_tasks()).pack(side="left", padx=5)

# 並び替え
sort_frame = tk.Frame(root)
sort_frame.pack(pady=5)

sort_label = tk.Label(sort_frame, text="日付：")
sort_label.pack(side="left")

sort_btn1 = tk.Button(sort_frame, text="昇順", command=lambda: set_sort_order("asc"))
sort_btn1.pack(side="left", padx=(0, 2))

sort_btn2 = tk.Button(sort_frame, text="降順", command=lambda: set_sort_order("desc"))
sort_btn2.pack(side="left", padx=(0, 20))

reset_btn = tk.Button(sort_frame, text="リセット", command=lambda: set_sort_order("none"))
reset_btn.pack(side="left")

# スクロール付きキャンバス
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
task_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=task_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

task_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# --- APIリクエスト共通 ---
def api_request(method, path="", data=None):
    try:
        response = requests.request(method, f"{BASE_URL}{path}", json=data)
        response.raise_for_status()

        # 204 No Content → 成功として True を返す
        if response.status_code == 204:
            return True

        # 通常のレスポンスは json で返す
        return response.json()
    except requests.RequestException as e:
        print(f"APIエラー: {e}")
        return None


# --- ファイル保存 ---
def save_to_file(tasks):
    with open(LOCAL_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def load_from_file():
    if os.path.exists(LOCAL_FILE):
        with open(LOCAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# --- 並び順 ---
sort_order = tk.StringVar(value="asc")

def set_sort_order(order):
    sort_order.set(order)
    fetch_tasks()

def reset_sort():
    sort_order.set("none")
    fetch_tasks()

# --- タスク取得 ---
def fetch_tasks():
    result = api_request("get")
    if result is not None:
        tasks = result  # 空リストOK
    else:
        tasks = load_from_file()

    if filter_var.get() == "done":
        tasks = [t for t in tasks if t.get("done")]
    elif filter_var.get() == "undone":
        tasks = [t for t in tasks if not t.get("done")]

    if filter_tag.get():
        tag = filter_tag.get().strip()
        tasks = [t for t in tasks if tag in t.get("tags", [])]

    if filter_date.get():
        try:
            fd = datetime.strptime(filter_date.get(), "%Y%m%d").strftime("%Y-%m-%d")
            tasks = [t for t in tasks if t.get("dueDate") == fd]
        except:
            messagebox.showwarning("日付形式", "YYYYMMDD で入力してください")

    if sort_order.get() == "asc":
        tasks.sort(key=lambda t: t.get("dueDate") or "9999-99-99")
    elif sort_order.get() == "desc":
        tasks.sort(key=lambda t: t.get("dueDate") or "0000-00-00", reverse=True)

    update_task_list(tasks)
    save_to_file(tasks)

# --- 追加 ---
def add_task():
    task = task_input.get().strip()
    due_raw = date_input.get().strip()
    tags_raw = tags_input.get().strip()

    if not task:
        messagebox.showwarning("警告", "タスクを入力してください。")
        return

    try:
        due_date = datetime.strptime(due_raw, "%Y%m%d").strftime("%Y-%m-%d") if due_raw else None
    except ValueError:
        messagebox.showerror("形式エラー", "日付は YYYYMMDD 形式で入力してください")
        return

    tags = [tag.strip() for tag in tags_raw.split(",") if tag.strip()]
    data = {"task": task, "done": False, "tags": tags, "dueDate": due_date}
    if api_request("post", data=data):
        task_input.set("")
        date_input.set("")
        tags_input.set("")
        fetch_tasks()

# --- 表示更新 ---
def update_task_list(tasks):
    global task_frame
    for widget in task_frame.winfo_children():
        widget.destroy()
    
    # canvas 上の古い task_frame を削除
    canvas.delete("all")
    task_frame.destroy()

    # 新しい Frame を再作成
    task_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=task_frame, anchor="nw")

    # 空リストでも問題なく更新できるように
    if not tasks:
        empty_label = tk.Label(task_frame, text="タスクはありません", font=("Arial", 12), fg="gray", width=50, anchor="center", justify="center")
        empty_label.pack(pady=10)
        return
    
        # --- ヘッダー行を追加 ---
    header = tk.Frame(task_frame)
    header.pack(anchor="w", fill="x", padx=10, pady=(0, 2))

    tk.Label(header, text="", width=2).pack(side="left")  # チェックボックス用スペース
    tk.Label(header, text="タスク", width=20, font=("Arial", 10, "bold")).pack(side="left", anchor="w")
    tk.Label(header, text="状態", width=6, font=("Arial", 10, "bold")).pack(side="left")
    tk.Label(header, text="タグ", width=15, font=("Arial", 10, "bold")).pack(side="left", anchor="w")
    tk.Label(header, text="期限", width=12, font=("Arial", 10, "bold")).pack(side="left", anchor="w")
    tk.Label(header, text="", width=10).pack(side="left")  # 編集/削除ボタン用スペース


    for task in tasks:
        row = tk.Frame(task_frame)
        row.pack(anchor="w", fill="x", padx=10, pady=2)

        is_done = task.get("done", False)
        due = task.get("dueDate")
        is_overdue = False
        if due:
            try:
                is_overdue = not is_done and datetime.strptime(due, "%Y-%m-%d").date() < datetime.today().date()
            except:
                pass

        fg_color = "gray" if is_done else ("red" if is_overdue else "black")
        font_style = ("Arial", 10, "overstrike") if is_done else ("Arial", 10)

        var = tk.BooleanVar(value=is_done)
        cb = tk.Checkbutton(
            row, variable=var,
            command=lambda t=task, v=var: toggle_done(t, v)
        )
        cb.pack(side="left")

        task_text = task.get("task", "")
        tags_text = ",".join(task.get("tags", []))
        due_text = task.get("dueDate") or ""

        label = tk.Label(row, text=task_text, font=font_style, fg=fg_color, width=20, anchor="w")
        label.pack(side="left")

        tk.Label(row, text="完了" if is_done else "未完了", width=6, fg=fg_color).pack(side="left")
        tk.Label(row, text=tags_text, width=15, anchor="w", fg=fg_color).pack(side="left")
        tk.Label(row, text=due_text, width=12, anchor="w", fg=fg_color).pack(side="left")

        tk.Button(row, text="編集", command=lambda t=task: edit_task(t)).pack(side="left", padx=3)
        tk.Button(row, text="削除", command=lambda tid=task["id"]: delete_task(tid)).pack(side="left", padx=3)

# --- 編集 ---
def edit_task(task):
    edit_win = tk.Toplevel(root)
    edit_win.title("編集項目の選択")
    edit_win.geometry("300x150+{}+{}".format(
        root.winfo_rootx() + root.winfo_width() // 2 - 150,
        root.winfo_rooty() + root.winfo_height() // 2 - 75
    ))
    choice = tk.StringVar(value="task")

    tk.Label(edit_win, text="何を編集しますか？").pack(pady=5)
    tk.Radiobutton(edit_win, text="タスク", variable=choice, value="task").pack(anchor="w", padx=10)
    tk.Radiobutton(edit_win, text="日付", variable=choice, value="date").pack(anchor="w", padx=10)
    tk.Radiobutton(edit_win, text="タグ", variable=choice, value="tag").pack(anchor="w", padx=10)

    def proceed():
        selected = choice.get()
        edit_win.destroy()

        if selected == "task":
            new = simpledialog.askstring("編集", "新しいタスク名：", initialvalue=task["task"])
            if new and new.strip():
                task["task"] = new.strip()

        elif selected == "date":
            new = simpledialog.askstring("編集", "新しい日付 (YYYYMMDD)：", initialvalue=(task.get("dueDate") or "").replace("-", ""))
            if new is not None:
                new = new.strip()
                if new == "":
                    task["dueDate"] = None
                else:
                    try:
                        task["dueDate"] = datetime.strptime(new, "%Y%m%d").strftime("%Y-%m-%d")
                    except:
                        messagebox.showwarning("日付形式", "正しい形式で入力してください")
                        return

        elif selected == "tag":
            new = simpledialog.askstring("編集", "新しいタグ（カンマ区切り）：", initialvalue=",".join(task.get("tags", [])))
            if new is not None:
                task["tags"] = [tag.strip() for tag in new.split(",") if tag.strip()]

        #PUTで送信
        data = {
            "id": task["id"],
            "task": task["task"],
            "done": task["done"],
            "tags": task.get("tags", []),
            "dueDate": task.get("dueDate")
        }
        if not api_request("put", f"/{task['id']}", data):
            messagebox.showerror("エラー", "編集に失敗しました")
        fetch_tasks()

    tk.Button(edit_win, text="決定", command=proceed).pack(pady=10)


# --- 完了切替 ---
def toggle_done(task, var):
    task["done"] = var.get()
    api_request("put", f"/{task['id']}", data=task)
    fetch_tasks()

# --- 削除 ---
def delete_task(task_id):
    if messagebox.askyesno("確認", "このタスクを削除しますか？"):
        result = api_request("delete", f"/{task_id}")
        if result is not None:
            fetch_tasks()  
        else:
            messagebox.showerror("エラー", "削除に失敗しました")

# --- 起動 ---
fetch_tasks()
root.mainloop()


