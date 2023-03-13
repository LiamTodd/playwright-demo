# Create your views here.
from django.shortcuts import redirect
# Create your views here.
from django.shortcuts import render

from .models import TodoListItem


def todoappView(request):
	all_todo_items = TodoListItem.objects.all()
	return render(request, 'todolist.html',
				  {'all_items': all_todo_items})


def addTodoView(request):
	x = request.POST['content']
	new_item = TodoListItem.objects.create(content=x)
	return redirect('index')


def deleteTodoView(request, i):
	y = TodoListItem.objects.get(id=i)
	y.delete()
	return redirect('index')
