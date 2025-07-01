package com.example.demo;

import java.util.Map;
import java.util.NoSuchElementException;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@ControllerAdvice 
public class GlobalExceptionHandler {
    @ExceptionHandler(NoSuchElementException.class) 
    @ResponseStatus(HttpStatus.NOT_FOUND)           
    @ResponseBody 
    public Map<String, String> handleNotFound(NoSuchElementException ex) {
        return Map.of("error", ex.getMessage());     // ❺ {"error": "メッセージ"} の形式で返す
    }
}
