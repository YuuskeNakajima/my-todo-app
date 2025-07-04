package com.example.demo;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class Todo {
    private int id;

    @NotBlank(message = "タスク名は必須です")
    @Size(max = 255, message = "タスク名は255文字以内です")
    private String task;

    private boolean done;

    private List<String> tags = new ArrayList<>();  
    private LocalDate dueDate;                      

    public Todo() {

    }

    public Todo(int id, String task, boolean done) {
        this.id = id;
        this.task = task;
        this.done = done;
    }

    public int getId() { 
        return id; 
    }

    public String getTask() { 
        return task; 
    }

    public boolean isDone() { 
        return done; 
    }

    public List<String> getTags() { 
        return tags;
     }
     
    public LocalDate getDueDate() { 
        return dueDate; 
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

    public void setTags(List<String> tags) {
         this.tags = tags; 
        }
    public void setDueDate(LocalDate dueDate) { 
        this.dueDate = dueDate; 
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Todo todo = (Todo) o;
        return id == todo.id;
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
