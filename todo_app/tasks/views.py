from django.core.management.base import BaseCommand
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from tasks.models import Task
from django.shortcuts import render

class Command(BaseCommand):
    help = 'Manage tasks'

    def add_arguments(self, parser):
        parser.add_argument('action', choices=['add', 'complete', 'list'])
        parser.add_argument('--name', type=str, help='Name of the task')
        parser.add_argument('--description', type=str, help='Description of the task')

    def handle(self, *args, **kwargs):
        action = kwargs['action']

        if action == 'add':
            name = kwargs['name']
            description = kwargs['description']
            Task.objects.create(name=name, description=description)
            self.stdout.write(self.style.SUCCESS(f'Task "{name}" added.'))

        elif action == 'complete':
            task = Task.objects.filter(name=kwargs['name']).first()
            if task:
                task.completed = True
                task.save()
                self.stdout.write(self.style.SUCCESS(f'Task "{task.name}" marked as complete.'))
            else:
                self.stdout.write(self.style.ERROR('Task not found.'))

        elif action == 'list':
            tasks = Task.objects.all()
            for task in tasks:
                status = '✅' if task.completed else '❌'
                self.stdout.write(f'{status} {task.name}: {task.description}')

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Task.objects.create(name=name, description=description)
        return redirect('task_list')
    return render(request, 'tasks/add_task.html')

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')


def home(request):
    return render(request, 'home.html')  # You can create a home.html file
