from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, LoginForm
from .models import *
from django.contrib.auth.models import Permission





@login_required(login_url="login")
def index_view(request):
    if request.user.is_authenticated :
        return render(request, 'Kanban/index.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


class LoginView(View):
    form_class = LoginForm
    template_name = 'Kanban/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('index'))
            else:
                # Return an 'invalid login' error message.
                form.add_error(None, 'Invalid username or password')
        return render(request, self.template_name, {'form': form})

class RegisterView(View):
    form_class = RegisterForm
    template_name = 'Kanban/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST,request.FILES)
        
        if form.is_valid():
            # save data before submit
            companyName = form.cleaned_data['company']
            userName = form.cleaned_data['username']
            # submit form
            form.save()

            # query that data
            query = User.objects.filter(company = companyName) # save company name
            
            # if company have only 1 member, change role to Admin 
            if len(query) == 1:

                get_username = User.objects.get(username = userName)
                get_username.role = 'A'
                get_username.save()
                
                if get_username.role == 'A':
                    permissions = Permission.objects.filter(codename__in=['CreateTeam', 
                                                                          'UpdateTeam', 
                                                                          'DeleteTeam',
                                                                          'CreateTask',
                                                                          'UpdateTask',
                                                                          'DeleteTask',
                                                                          'CreateSubTask',
                                                                          'UpdateSubTask',
                                                                          'DeleteSubTask'])
                    get_username.user_permissions.set(permissions)
                else:
                    permissions = Permission.objects.filter(codename__in = ['UpdateTask',
                                                                            'CreateSubTask',
                                                                            'UpdateSubTask',
                                                                            'DeleteSubTask'])
                    get_username.user_permissions.set(permissions)
            
            return HttpResponseRedirect(reverse('index'))  # Redirect to a success page
        return render(request, self.template_name, {'form': form})

"""
    Feature to implement 
    
    - Create / Update / Delete Task and subtask 
    - Change roles (Team leader or member) 
    - Create / Update/ Delete Team 
    - Invite member (Admin only)

"""