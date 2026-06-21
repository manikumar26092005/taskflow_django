from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CategoryForm, RegisterForm, TaskForm
from .models import Category, Task


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "field-input", "placeholder": "Username", "autofocus": True}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "field-input", "placeholder": "Password"}
        )


class TaskFlowLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = StyledAuthenticationForm
    redirect_authenticated_user = True


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Account created. Welcome to TaskFlow!")
        return response


@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "all")
    priority = request.GET.get("priority", "all")
    category_id = request.GET.get("category", "all")

    if search:
        tasks = tasks.filter(title__icontains=search)
    if status == "pending":
        tasks = tasks.filter(is_completed=False)
    elif status == "completed":
        tasks = tasks.filter(is_completed=True)
    if priority in {"low", "medium", "high"}:
        tasks = tasks.filter(priority=priority)
    if category_id not in {"all", ""}:
        tasks = tasks.filter(category_id=category_id)

    all_tasks = Task.objects.filter(owner=request.user)
    context = {
        "tasks": tasks,
        "total_count": all_tasks.count(),
        "pending_count": all_tasks.filter(is_completed=False).count(),
        "completed_count": all_tasks.filter(is_completed=True).count(),
        "categories": Category.objects.filter(owner=request.user),
        "search": search,
        "status": status,
        "priority": priority,
        "category_id": category_id,
    }
    return render(request, "tasks/task_list.html", context)


@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST, owner=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            form.instance = task
            form.save()
            messages.success(request, "Task added successfully!")
            return redirect("task_list")
    else:
        form = TaskForm(owner=request.user)
    return render(request, "tasks/task_form.html", {"form": form, "mode": "add"})


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, owner=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect("task_list")
    else:
        form = TaskForm(instance=task, owner=request.user)
    return render(
        request, "tasks/task_form.html", {"form": form, "mode": "edit", "task": task}
    )


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted.")
        return redirect("task_list")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})


@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    task.is_completed = True
    task.save(update_fields=["is_completed"])
    messages.success(request, f'"{task.title}" marked as done.')
    return redirect("task_list")


@login_required
def category_list(request):
    categories = Category.objects.filter(owner=request.user)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.owner = request.user
            category.save()
            messages.success(request, "Category created.")
            return redirect("category_list")
    else:
        form = CategoryForm()
    return render(
        request,
        "tasks/category_list.html",
        {"categories": categories, "form": form},
    )


@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, owner=request.user)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted.")
    return redirect("category_list")
