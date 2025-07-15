# ToDoアプリ

このアプリは、Windows向けのタスク管理ツールです。  
実行ファイル（exe）からJavaサーバー（server.jar）を起動し、タスクの追加・編集・削除ができます。

## 📦 内容

- main.exe        : GUIアプリ本体（Python製、PyInstallerビルド済み）
- server.jar      : タスク管理用のJavaバックエンド（Spring Bootなど）
- todos.json      : タスク情報のローカル保存ファイル

## ✅ 使い方

1. `main.exe` をダブルクリックして起動
2. 自動で `server.jar` が起動します（Javaが必要です）
3. GUI上でタスクの追加・完了チェック・削除などが行えます

## 🔧 動作環境

- Windows 10 / 11
- Java 17 以上（JREでも可）

## 📌 注意事項

- `server.jar` を同じフォルダに置いてください
- Javaがインストールされていない場合は動作しません
