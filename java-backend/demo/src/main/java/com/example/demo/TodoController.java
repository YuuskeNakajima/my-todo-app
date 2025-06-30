package com.example.demo;

import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/todos")
public class TodoController {

    private List<Todo> todos = new ArrayList<>(List.of(
        new Todo(1,"牛乳を買う",false),
        new Todo(2,"卵を買う",true)
    ));

    @GetMapping
    public List<Todo> getTodos() {
        return todos;
    }

    @PostMapping
    public Todo addTodo(@RequestBody Todo newtodo) {
        todos.add(newtodo);
        return newtodo;
    }

    @DeleteMapping("/{todoId}")
    public void deleteTodo(@PathVariable int todoId) {
        todos.removeIf(todo -> todo.getId() == todoId);
    }
    @PutMapping("/{todoId}")
    public Todo updateTodo(@PathVariable int todoId, @RequestBody Todo updatedTodo) {
        for(int i = 0; i < todos.size(); i++) {
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
    
}
