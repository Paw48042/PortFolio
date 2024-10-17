from django.urls import path, include
from .views import *#RegisterView, LoginView, index_view, logout_view
from .api.views import *
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path("", index_view , name = 'index'),
    path("register",RegisterView.as_view(template_name = "Kanban/register.html"), name = 'register' ),
    path("login",LoginView.as_view(template_name = "Kanban/login.html"), name = "login" ),
    path("logout", logout_view, name = "logout"),

    # API Route for task
    path("api/get_task", get_task, name = "get_task"),
    path("api/get_one_task/<int:task_id>",get_one_task, name = "get_one_task"),
    path("api/get_user",get_user, name = "get_user"),
    path("api/create_task", create_task, name = "create_task"),
    path("api/edit_task/<int:task_id>", edit_task, name = "edit_task"),
    path("api/make_progress/<str:task_id>",make_progress, name = "make_progress"),
    path("api/delete_task/<str:task_id>", delete_task, name = "delete_task"),

    # API Route for user 
    path("api/update_role/<str:target_id>", update_role, name = 'update_role'),
    path("api/delete_user/<str:target_id>", delete_user, name = 'delete_user'),

    # API Route for comment 
    path("api/get_comment/<str:task_id>", get_comment, name = 'get_comment'),
    path("api/post_comment/<str:task_id>", post_comment,name=  'post_comment')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)