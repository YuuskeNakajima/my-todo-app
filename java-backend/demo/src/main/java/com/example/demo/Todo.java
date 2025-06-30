package com.example.demo;

public class Todo {
    private int id;
    private String task;

    public Todo(int id, String task){
        this.id = id;
        this.task = task;
    }

    public int getId(){
        return id;
    }

    public String getTask(){
        return task;
    }
}
