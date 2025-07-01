import requests

def get_todos(filter_done=None):
    response = requests.get("http://localhost:8080/todos")
    if response.status_code == 200:
        todos = response.json()
        for todo in todos:
            if filter_done is None or todo["done"] == filter_done:
                print(f"ID: {todo['id']} / タスク: {todo['task']} / 完了: {todo['done']}")
    else:
        print("タスクの取得に失敗しました")

def add_todo(task, done):
    data = {
        "task": task,
        "done": done
    }

    response = requests.post("http://localhost:8080/todos", json=data)
    if response.status_code == 200:
        print("タスクを追加しました")
    else:
        print("タスクの追加に失敗しました")

def delete_todo():
    todo_id = int(input("削除するタスクのIDを入力してください: "))
    response = requests.delete(f"http://localhost:8080/todos/{todo_id}")
    if response.status_code == 200 or response.status_code == 204:
        print("タスクを削除しました")
    else:
        print(f"削除に失敗しました。ステータスコード: {response.status_code}")

def get_todo_by_id():
    todo_id = int(input("詳細を確認したいタスクのIDを入力してください: "))
    response = requests.get(f"http://localhost:8080/todos/{todo_id}")
    if response.status_code == 200:
        todo = response.json()
        print(f"ID: {todo['id']} / タスク: {todo['task']} / 完了: {todo['done']}")
    else:
        print(f"タスクが見つかりません（ステータスコード: {response.status_code}）")


def update_todo():
    todo_id = int(input("更新したいタスクのIDを入力してください: "))
    task = input("新しいタスクを入力してください: ")
    done_str = input("完了していますか？ (yes/no): ")
    done = done_str.lower() == "yes"

    updated_data = {
        "id": todo_id,
        "task": task,
        "done": done
    }

    response = requests.put(f"http://localhost:8080/todos/{todo_id}", json=updated_data)
    if response.status_code == 200:
        print("タスクを更新しました。")
    else:
        print(f"更新に失敗しました（ステータスコード: {response.status_code}）")

def filter_todos():
    status = input("表示するタスクの種類を選んでください (done/undone): ").lower()
    response = requests.get("http://localhost:8080/todos")
    if response.status_code == 200:
        todos = response.json()
        if status == "done":
            filtered = [todo for todo in todos if todo["done"]]
        elif status == "undone":
            filtered = [todo for todo in todos if not todo["done"]]
        else:
            print("無効な入力です。")
            return
        for todo in filtered:
            print(f"ID: {todo['id']} / タスク: {todo['task']} / 完了: {todo['done']}")
    else:
        print("タスクの取得に失敗しました")
    
    def toggle_todo():
        todo_id = int(input("完了状態を切り替えたいタスクのIDを入力してください: "))
        response = requests.patch(f"http://localhost:8080/todos/{todo_id}/toggle")
        if response.status_code == 200:
            print("完了状態を切り替えました。")
        else:
            print(f"切り替えに失敗しました（ステータスコード: {response.status_code}）")


print("現在のタスク一覧:")
get_todos()

print("\n新しいタスクを追加します:")
add_todo("Pythonで追加", False)

print("\n追加後のタスク一覧:")
get_todos()

while True:
    print("\nメニュー:")
    print("1. タスク一覧表示")
    print("2. タスク追加")
    print("3. タスク削除")
    print("4. タスクの詳細表示")
    print("5. タスクの更新")
    print("6. 終了")
    print("7. 完了したタスクを表示")
    print("8. 未完了のタスクを表示")
    print("9. 完了状態を切り替え")    

    choice = input("番号を選んでください: ")

    if choice == "1":
        get_todos()
    elif choice == "2":
        task = input("タスク内容を入力してください: ")
        done_str = input("完了していますか？ (yes/no): ")
        done = done_str.lower() == "yes"
        add_todo(task, done) 
    elif choice == "3":
        delete_todo()
    elif choice == "4":
        get_todo_by_id()
    elif choice == "5":
        update_todo()
    elif choice == "6":
        print("終了します。")
        break
    elif choice == "7":
        get_todos(filter_done=True)
    elif choice == "8":
        get_todos(filter_done=False)
    elif choice == "9":
        toggle_todo()
    else:
        print("無効な入力です。")