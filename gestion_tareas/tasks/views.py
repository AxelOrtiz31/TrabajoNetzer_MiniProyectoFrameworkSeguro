from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm

@login_required
def dashboard(request):
    """Vista principal según el rol."""
    if request.user.is_staff:
        # Admin ve todas las tareas
        tasks = Task.objects.all().order_by('-created_at')
    else:
        # Usuario normal solo sus tareas
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tasks/dashboard.html', {'tasks': tasks})

@login_required
def task_list(request):
    """Listado detallado de tareas (similar a dashboard pero con más opciones)."""
    if request.user.is_staff:
        tasks = Task.objects.all().order_by('-created_at')
    else:
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    """Crear una nueva tarea (POST protegido con CSRF por Django)."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Tarea creada correctamente.')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'accion': 'Crear'})

@login_required
def task_edit(request, pk):
    """Editar tarea existente. Solo el propietario o admin pueden editar."""
    task = get_object_or_404(Task, pk=pk)
    # Verificar permisos: solo admin o propietario
    if not request.user.is_staff and task.user != request.user:
        messages.error(request, 'No tienes permiso para editar esta tarea.')
        return redirect('task_list')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea actualizada correctamente.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'accion': 'Editar'})

@staff_member_required  # Solo admin puede eliminar (opcional)
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Tarea eliminada.')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})