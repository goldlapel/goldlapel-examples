import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Todo


@csrf_exempt
@require_http_methods(["GET", "POST"])
def todo_list(request):
    if request.method == "GET":
        todos = list(Todo.objects.values("id", "title", "done").order_by("id"))
        return JsonResponse(todos, safe=False)

    body = json.loads(request.body)
    todo = Todo.objects.create(
        title=body["title"],
        done=body.get("done", False),
    )
    return JsonResponse({"id": todo.id, "title": todo.title, "done": todo.done}, status=201)
