<?php

namespace App\Http\Controllers;

use App\Models\Todo;
use Illuminate\Http\Request;

class TodoController
{
    public function index()
    {
        return Todo::all();
    }

    public function store(Request $request)
    {
        $todo = Todo::create($request->only(['title', 'done']));
        return response()->json($todo, 201);
    }
}
