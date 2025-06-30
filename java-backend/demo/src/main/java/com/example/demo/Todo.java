package com.example.demo;

public class Todo {
    private int id;
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
