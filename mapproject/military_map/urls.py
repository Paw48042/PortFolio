from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from .views import *



urlpatterns = [
    # User Create, Update, Delete.
    path("register", Register.as_view(), name = "register"),
    path('update/profile/<int:pk>', UpdateUser.as_view(),name = "update_profile"), 
    path('delete/profile/<int:pk>', DeleteUser.as_view(), name = "delete_user"),
    # -----------------------------------------------------------------------------------#

    # Login - Logout
    path("login/", LoginView.as_view(template_name = 'military_map/login.html', # Login view is pre written by django
                                     next_page = 'mission', 
                                     authentication_form = LoginForm,
                                     redirect_authenticated_user = True), name = 'login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'), # Logout view is pre written by django
    # -----------------------------------------------------------------------------------#
    
    # View Mission, Create Mission, Delete Mission
    path("mission",MissionView.as_view(),name = "mission"),
    path("mission/create", CreateMission.as_view(), name = "create_mission"),
    path('mission/delete/<int:id>', DeleteMission.as_view(), name='delete_mission'),
    path('mission/join/<int:id>',JoinMission.as_view(),name = 'join_mission'), # <int:id> is for mission id
    # -----------------------------------------------------------------------------------#
    
    # Other View
    path('', HomepageView.as_view(), name = 'home'),
    path('instruction', InstructionView.as_view(), name = 'instruction'),
    #path("index", TestView.as_view(), name = "index"),
    #path("map", MainMap.as_view(), name = "map_view"),
    
    # API
    path('get_one_drawing/<int:id>', get_one_drawing, name = 'get_one_drawing'), 
    path('get_drawings/<int:id>', get_drawings, name='get_drawings'),
    path('save_drawing/<int:id>', save_drawing, name='save_drawing'),
    path('delete_drawing/<int:id>', delete_drawing, name = 'delete_drawing'),
    path('edit_drawing/<int:id>', edit_drawings, name = 'edit_drawings'),
 
]

