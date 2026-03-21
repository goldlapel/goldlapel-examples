package com.example;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/todos")
public class TodoController {

    private final TodoRepository repo;

    TodoController(TodoRepository repo) {
        this.repo = repo;
    }

    @GetMapping
    List<Todo> list() {
        return repo.findAll();
    }

    @PostMapping
    Todo create(@RequestBody Todo todo) {
        return repo.save(todo);
    }
}
