package com.example.demo;

import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
public class TodoController {

    private List<Todo> todos = new ArrayList<>();

    @GetMapping("/todos")
    public List<Todo> getTodos() {
        return List.of(
            new Todo(1, "買い物に行く"),
            new Todo(2, "宿題をやる"),
            new Todo(3, "運動する")
        );
    }
}
