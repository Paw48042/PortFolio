from django.db.models.base import Model as Model 
from django.shortcuts import render, redirect, get_object_or_404 
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, Http404
from django.contrib.gis.geos import GEOSGeometry
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, DeleteView
from .models import *
from .forms import  RegisterForm, CreateMissionForm 
import json

# Views without authentication
# LoginView
# LogoutView 

class InstructionView(TemplateView):
    template_name = 'military_map/instruction.html'

class HomepageView(TemplateView):
    template_name = 'military_map/home.html'


# Views with authentication 

class MainMap(LoginRequiredMixin,TemplateView):
    
    template_name = 'military_map/map.html'
    login_url = reverse_lazy('login')
    
"""class TestView(LoginRequiredMixin,TemplateView):
    
    template_name = 'military_map/index.html'
    login_url = reverse_lazy('login')
"""
  
class MissionView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('login')
    template_name = 'military_map/mission.html'
    model = Mission


""" User  CRUD """
# Create

class Register(SuccessMessageMixin,CreateView):
    template_name = 'military_map/register.html'
    success_url = reverse_lazy('login')
    form_class = RegisterForm
    success_message = "Your profile was created successfully"

# Update 

class UpdateUser(LoginRequiredMixin,UpdateView):
    template_name = "military_map/update_user.html"
    model = CustomUser
    fields = ['email','first_name', 'last_name']
    error_message = "You don't have permission to update this page"

    def get_object(self, queryset = None):
        user_id = self.kwargs['pk']
        if self.request.user.id != user_id:
            raise PermissionDenied(self.error_message)
        return get_object_or_404(CustomUser, pk=user_id)
    def get_success_url(self):
        return reverse_lazy("update_profile", kwargs={'pk': self.object.pk})
    
# Delete 

class DeleteUser(LoginRequiredMixin,DeleteView):
    template_name = "military_map/confirm_delete.html"
    model = CustomUser
    success_url = reverse_lazy("home")
    error_message = "You don't have permission to delete this user"

    def get_object(self, queryset = None):
        user_id = self.kwargs['pk']
        if self.request.user.id != user_id:
            raise PermissionDenied(self.error_message)
        return get_object_or_404(CustomUser, pk=user_id)
    

""" Mission CRUD """
# Create
class CreateMission(LoginRequiredMixin, CreateView):
    template_name = 'military_map/create_mission.html'
    success_url = reverse_lazy('mission')
    success_message = "Mission Created Successfully"
    form_class = CreateMissionForm

    def form_valid(self, form):
        form.instance.createBy = self.request.user
        return super().form_valid(form)

# Delete
class DeleteMission(LoginRequiredMixin, DeleteView):
    template_name = 'military_map/confirm_delete_mission.html'
    success_url = reverse_lazy('mission')
    model = Mission
    error_message = "You don't have permission to delete this mission"

    def get_object(self, queryset = None):
        # Get the mission 
        object = get_object_or_404(Mission, pk = self.kwargs['id']) 
        if object.createBy.id != self.request.user.id:
            raise PermissionDenied(self.error_message)
        return object

# Go into the mission room (Kind of like the chat room)
class JoinMission(LoginRequiredMixin,DetailView): # AKA join chatroom
    
    template_name = 'military_map/mission_map.html'
    model = Mission

    def get_object(self, queryset = None):
        # Get the mission 
        mission = get_object_or_404(Mission, pk = self.kwargs.get('id'))
        return mission



def get_one_drawing(request, id): 
    
    drawing = Drawing.objects.get(pk = id)
    geom = json.loads(drawing.geom.geojson) # Convert GEOSGeometry to GeoJSON
    features = []
    features.append({
        'type': 'Feature',
            'geometry': geom,
            'properties': {
                'drawing_id' : drawing.id,
                'name': drawing.name,
                'mission_id': drawing.mission.id,
                'color': drawing.properties.get('color', None),  # Add color property
                'fillColor': drawing.properties.get('fillColor', None),  # Add fillColor property
            }
    })
    feature_collection = {
        'type': 'FeatureCollection',
        'features': features
    }
    return JsonResponse(feature_collection)

# Create draw object 
def get_drawings(request, id):
    # Retrieve all drawings
    mission = Mission.objects.get(pk = id)
    drawings = Drawing.objects.filter(mission = mission)
    features = []
    
    for drawing in drawings:
        geom = json.loads(drawing.geom.geojson)  # Convert GEOSGeometry to GeoJSON
        features.append({
            'type': 'Feature',
            'geometry': geom,
            'properties': {
                'drawing_id' : drawing.id,
                'name': drawing.name,
                'mission_id': drawing.mission.id,
                'color': drawing.properties.get('color', None),  # Add color property
                'fillColor': drawing.properties.get('fillColor', None),  # Add fillColor property
            }
        })
    
    feature_collection = {
        'type': 'FeatureCollection',
        'features': features
    }
    
    return JsonResponse(feature_collection)

# Handle post drawing 
def save_drawing(request, id):
    
    if request.method == "POST":

        # loads the data  
        data = json.loads(request.body.decode('utf-8'))  # Decode and parse the JSON data
        mission = get_object_or_404(Mission, pk = id)
        # handle geojson from fetching
        try:
            
            # Convert the geometry part to a JSON string and then to a GEOSGeometry object
            #geojson_str = json.dumps(data['geometry'])
            geom = GEOSGeometry(json.dumps(data['geometry']))

            # Create and save the drawing
            drawing = Drawing.objects.create(
                geom=geom,
                name=data.get('name', 'Unnamed'),
                mission=mission,
                properties = data.get('properties', {})
            )

            # return success message
            return JsonResponse({'status': 'success', 'id': drawing.id}) 
        
        except Exception as e:
            return JsonResponse({'status': 'fail', 'error': str(e)}, status=400)
    
    # If not post, then fail
    return JsonResponse({'status': 'fail'}, status=400)


def delete_drawing(request, id):

    to_delete_id = id
    drawing = get_object_or_404(Drawing, pk = id)

    # If delete request. 
    if request.method == 'DELETE':
        
        # Delete the object 
        drawing.delete() 

        return JsonResponse({
            'status' : 'success',
            'drawing_id' : to_delete_id,
            })
    return JsonResponse({'status': 'fail'}, status=400)

def edit_drawings(request, id):
    
    if request.method == 'PUT':

        try:
         # loads the data  
            data = json.loads(request.body.decode('utf-8'))  # Decode and parse the JSON data
            # handle geojson from fetching

            geom = GEOSGeometry(json.dumps(data['geometry']))

            drawing = get_object_or_404(Drawing, pk = id)
            drawing.geom = geom
            drawing.save()

            return JsonResponse({'status': 'Update Success', 'id': drawing.id})

        except Exception as e:
             return JsonResponse({'status': 'fail', 'error': str(e)}, status=400) 
        
