import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from myapp.models import Task, Status

# Create your views here.
def home(request):
    return render(request, 'home.html')

def create_task(request):
    if request.method == 'POST':
        name: str = request.POST.get('task-name', '')
        description: str = request.POST.get('task-description', '').strip()
        status_id: Status = Status.objects.get(name='Pendiente')

        deadline_str: str = request.POST.get('task-deadline', '').strip()
        deadline: datetime.datetime = None

        if deadline_str:
            try:
                deadline = datetime.datetime.strptime(deadline_str, '%Y-%m-%d')

            except ValueError:
                pass

        Task.objects.create(
            name=name,
            description=description,
            deadline=deadline,
            status_id=status_id,
        )

        messages.success(request, '¡Tarea creada exitosamente!')

        return redirect('list-tasks')

    return render(request, 'create_task.html')

def list_tasks(request):
    return render(request, 'list_tasks.html', {
        'tasks': Task.objects.all(),
    })

def edit_task(request, task_id):
    if request.method == 'POST':
        task: Task = Task.objects.get(id=task_id)

        task.name = request.POST.get('task-name', '')
        task.description = request.POST.get('task-description', '').strip()
        task.status_id = Status.objects.get(id=int(request.POST.get('task-status', 0)))

        deadline_str: str = request.POST.get('task-deadline', '').strip()
        deadline: datetime.datetime = None

        if deadline_str:
            try:
                deadline = datetime.datetime.strptime(deadline_str, '%Y-%m-%d')

            except ValueError:
                pass

        task.deadline = deadline
        task.save()

        messages.success(request, '¡Tarea actualizada exitosamente!')

        return redirect('list-tasks')

    return render(request, 'edit_task.html', {
        'task': Task.objects.get(id=task_id),
        'task_statuses': Status.objects.all(),
    })

def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()

    messages.success(request, '¡Tarea eliminada exitosamente!')

    return redirect('list-tasks')