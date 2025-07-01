package com.example.demo;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
public class Todo {
    private int id;

    @NotBlank(message = "タスク名は必須です")
    @Size(max = 255, message = "タスク名は255文字以内です")
    private String task;
    private boolean done;

    public Todo(int id, String task, boolean done) {
        this.id = id;
        this.task = task; 
        this.done = done;
    }

    public int getId(){
        return id;
    }

    public String getTask(){
        return task;
    }

    public boolean isDone(){
        return done;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setTask(String task) {
        this.task = task;
    }

    public void setDone(boolean done) {
        this.done = done;
    }
}
