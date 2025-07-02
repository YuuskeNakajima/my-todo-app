import requests

BASE_URL = "http://localhost:8080/todos"

def request(method, url_suffix="", data=None):
    try:
        response = requests.request(method, f"{BASE_URL}{url_suffix}", json=data)
        response.raise_for_status()
        if response.status_code != 204:
            return response.json()
    except requests.RequestException as e:
        print(f"[エラー] {e}")
    return None

def get_todos(filter_done=None):
    todos = request("get")
    if not todos:
        print("タスクの取得に失敗しました")
        return
    for todo in todos:
        if filter_done is None or todo["done"] == filter_done:
            print(f"ID: {todo['id']} / タスク: {todo['task']} / 完了: {todo['done']}")

def add_todo(task, done=False):
    if not task.strip():
        print("タスク内容を入力してください")
        return
    if request("post", data={"task": task, "done": done}):
        print("タスクを追加しました")

def delete_todo():
    todo_id = input("削除するタスクID: ")
    if request("delete", f"/{todo_id}") is None:
        print("削除に失敗しました")

def get_todo_by_id():
    todo_id = input("確認するタスクID: ")
    todo = request("get", f"/{todo_id}")
    if todo:
        print(f"ID: {todo['id']} / タスク: {todo['task']} / 完了: {todo['done']}")
    else:
        print("タスクが見つかりません")

def update_todo():
    todo_id = input("更新するタスクID: ")
    task = input("新しいタスク内容: ")
    done = input("完了していますか？ (yes/no): ").lower() == "yes"
    data = {"id": int(todo_id), "task": task, "done": done}
    if request("put", f"/{todo_id}", data):
        print("更新しました")

def toggle_todo():
    todo_id = input("切り替えるタスクID: ")
    if request("patch", f"/{todo_id}/toggle"):
        print("完了状態を切り替えました")

def filter_todos():
    status = input("表示する種類 (done/undone): ").lower()
    if status not in {"done", "undone"}:
        print("無効な入力です")
        return
    get_todos(filter_done=(status == "done"))

def menu():
    while True:
        print("\n--- メニュー ---")
        print("1. 一覧  2. 追加  3. 削除  4. 詳細  5. 更新  6. 終了")
        print("7. 完了表示  8. 未完了表示  9. 完了切替")
        choice = input("番号を選択: ")
        if choice == "1": get_todos()
        elif choice == "2":
            task = input("タスク内容: ")
            done = input("完了？(yes/no): ").lower() == "yes"
            add_todo(task, done)
        elif choice == "3": delete_todo()
        elif choice == "4": get_todo_by_id()
        elif choice == "5": update_todo()
        elif choice == "6":
            print("終了します")
            break
        elif choice == "7": get_todos(filter_done=True)
        elif choice == "8": get_todos(filter_done=False)
        elif choice == "9": toggle_todo()
        else: print("無効な入力です")

if __name__ == "__main__":
    print("現在のタスク一覧:")
    get_todos()
    menu()