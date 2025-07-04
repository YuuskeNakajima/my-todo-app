package com.example.demo;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;
import java.util.*;
import jakarta.validation.Valid;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/todos")
public class TodoController {

    private int nextId = 1;
    private List<Todo> todos = new ArrayList<>();

    // バリデーションエラー処理
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public String handleValidationExceptions(MethodArgumentNotValidException ex) {
        return ex.getBindingResult()
                 .getFieldErrors()
                 .stream()
                 .map(error -> error.getField() + ": " + error.getDefaultMessage())
                 .findFirst()
                 .orElse("不正な入力です");
    }

    // 一覧取得
    @GetMapping
    public List<Todo> getTodos() {
        return todos;
    }

    // 新規追加
    @PostMapping
    public Todo addTodo(@Valid @RequestBody Todo newTodo) {
        newTodo.setId(nextId++);
        todos.add(newTodo);
        return newTodo;
    }

    // 削除
    @DeleteMapping("/{todoId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteTodo(@PathVariable int todoId) {
        boolean removed = todos.removeIf(todo -> todo.getId() == todoId);
        if (!removed) {
            throw new NoSuchElementException("指定されたIDのタスクが見つかりません: " + todoId);
        }
    }

    // 更新
    @PutMapping("/{todoId}")
    public Todo updateTodo(@PathVariable int todoId, @Valid @RequestBody Todo updatedTodo) {
        for (int i = 0; i < todos.size(); i++) {
            if (todos.get(i).getId() == todoId) {
                updatedTodo.setId(todoId);  // ID整合性
                todos.set(i, updatedTodo);
                return updatedTodo;
            }
        }
        throw new NoSuchElementException("指定されたIDのタスクが見つかりません: " + todoId);
    }

    // IDで取得
    @GetMapping("/{todoId}")
    public Todo getTodoById(@PathVariable int todoId) {
        for (Todo todo : todos) {
            if (todo.getId() == todoId) {
                return todo;
            }
        }
        throw new NoSuchElementException("指定されたIDのタスクが見つかりません: " + todoId);
    }

    // 完了状態の切り替え
    @PatchMapping("/{todoId}/toggle")
    public Todo toggleTodoDone(@PathVariable int todoId) {
        for (Todo todo : todos) {
            if (todo.getId() == todoId) {
                todo.setDone(!todo.isDone());
                return todo;
            }
        }
        throw new NoSuchElementException("指定されたIDのタスクが見つかりません: " + todoId);
    }
}
