from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("add/", views.add_task, name="add_task"),
    path("edit/<int:pk>/", views.edit_task, name="edit_task"),
    path("delete/<int:pk>/", views.delete_task, name="delete_task"),
    path("complete/<int:pk>/", views.complete_task, name="complete_task"),
    path("categories/", views.category_list, name="category_list"),
    path(
        "categories/delete/<int:pk>/",
        views.delete_category,
        name="delete_category",
    ),
    path("login/", views.TaskFlowLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
]
