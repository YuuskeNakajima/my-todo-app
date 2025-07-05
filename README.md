# ToDoアプリ（Python × Spring Boot）

## 🔧 起動方法

### 1. バックエンド（Spring Boot）
- Java 17 以上が必要です。

cd backend
./mvnw spring-boot:run
または .jar をビルドして実行：

./mvnw clean package
java -jar target/demo.jar
2. フロントエンド（Python）
Python 3.10 以上が必要です。

必要なライブラリをインストール：

pip install requests
python app.py
✅ 機能
タスクの追加／編集／削除

タグ・日付付き管理

完了の切り替え

並び替え・フィルタリング

ローカル保存（todos.json）

📌 備考
todos.json によりバックエンドなしでも表示可

GUIは × ボタンで終了可能です

---
