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

    private int nextId = 3;

    private List<Todo> todos = new ArrayList<>(List.of(
            new Todo(1, "牛乳を買う", false),
            new Todo(2, "卵を買う", true)));

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

    @GetMapping
    public List<Todo> getTodos() {
        return todos;
    }

    @PostMapping
    public Todo addTodo(@Valid @RequestBody Todo newTodo) {
        newTodo.setId(nextId++);
        todos.add(newTodo);
        return newTodo;
    }

    @DeleteMapping("/{todoId}")
    public void deleteTodo(@PathVariable int todoId) {
        todos.removeIf(todo -> todo.getId() == todoId);
    }

    @PutMapping("/{todoId}")
    public Todo updateTodo(@PathVariable int todoId, @RequestBody Todo updatedTodo) {
        for (int i = 0; i < todos.size(); i++) {
            if (todos.get(i).getId() == todoId) {
                todos.set(i, updatedTodo);
                return updatedTodo;
            }
        }
        throw new NoSuchElementException("指定されたIDのタスクが見つかりません: " + todoId);
    }

    @GetMapping("/{todoId}")
    public Todo getTodoById(@PathVariable int todoId) {
        for (Todo todo : todos) {
            if (todo.getId() == todoId) {
                return todo;
            }
        }
        throw new NoSuchElementException("指定されたIDのタスクが見つかりません: " + todoId);
    }

    @PatchMapping("/{todoId}/toggle")
    public Todo toggleTodoDone(@PathVariable int todoId) {
        for (Todo todo : todos) {
         if (todo.getId() == todoId) {
             todo.setDone(!todo.isDone()); // 状態を反転
                return todo;
            }
        }
        throw new NoSuchElementException("指定されたIDのタスクが見つかりません: " + todoId);
    }


}
