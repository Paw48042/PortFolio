from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.contrib.auth.decorators import login_required
from ..serializers import *
from django.db.models import Q


"""
This api is to send all the task to the front end
"""
@login_required(login_url="login")
@api_view(['GET'])
def get_task(request):
    user = User.objects.get(username = request.user.username)
    if request.method == 'GET':

        # if user is admin, can see all the task
        if request.user.role == 'A':
            queryset = Task.objects.filter(createBy__company = user.company)

            # Serialize the data
            serializer = TaskSerializer(queryset, many=True)

            # Return serialized data as JSON response
            return Response(serializer.data)
        
        # if user is team leader or member, can only see and interact with assigned task
        else:
            queryset = Task.objects.filter(Q(assigned=user) | Q(createBy=user)).distinct()
            
            # Serialize the data
            serializer = TaskSerializer(queryset, many=True)

            # Return serialized data as JSON response
            return Response(serializer.data)

"""
Get one task 
"""
@login_required(login_url='login')
@api_view(['GET'])
def get_one_task(request, task_id):
    
    # get task from id
    task = Task.objects.get(id = task_id)
    serializer = TaskSerializer(task, many = False)
    return Response(serializer.data)

"""
To get all user in the company
"""
@login_required(login_url='login')
@api_view(['GET'])
def get_user(request):
    user = User.objects.get(username = request.user.username)
    all_user = User.objects.filter(company = user.company)

    serializer = UserSerializer(all_user, many = True)

    return Response(serializer.data)



"""
To create new task, admin only
any POST PUT DELETE need to add this csrf token into the post, becausse of session base login stuff
https://docs.djangoproject.com/en/5.0/howto/csrf/#using-csrf-protection-with-ajax
"""

@login_required(login_url='login')   
@api_view(['POST'])
def create_task(request):
    if request.method == "POST":

        # Get serializer from model serializer
        serializer = CreateTaskSerializer(data = request.data)
        # Check if serializer is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
To update progress
"""

@login_required(login_url= 'login')
@api_view(['PUT'])
def make_progress(request, task_id):
    
    try:
        # Query for task
        task = Task.objects.get(pk = task_id)
    except Task.DoesNotExist:
        # If task not found
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # If found, check for the method
    if request.method == "PUT":
        serializer = UpdateTaskSerializer(task , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url= 'login')
@api_view(['PUT'])
def edit_task(request, task_id):
    
    try:
        # Query for task
        task = Task.objects.get(pk = task_id)
    except Task.DoesNotExist:
        # If task not found
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # If found, check for the method
    if request.method == "PUT":
        serializer = EditTaskSerializer(task , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
To Delete task
"""
@login_required(login_url = 'login')
@api_view(['DELETE'])
def delete_task(request, task_id):

    user = User.objects.get(username = request.user.username)
    try:
        # Query for task
        task = Task.objects.get(id = task_id)
    except Task.DoesNotExist:
        # If task not found
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # if found, check for the method
    if request.method == "DELETE":
        task.delete()
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)






"""
To update role, admin only
any POST PUT DELETE need to add this csrf token into the post, becausse of session base login stuff
https://docs.djangoproject.com/en/5.0/howto/csrf/#using-csrf-protection-with-ajax
"""
@login_required(login_url='login')
@api_view(['PUT'])
def update_role(request, target_id):
    try:
        target_user = User.objects.get(id = target_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # if put request and admin is update 
    if request.method == 'PUT' and request.user.role == 'A':
        serializer = UpdateRoleSerializer(target_user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
To delete role, admin only
any POST PUT DELETE need to add this csrf token into the post, becausse of session base login stuff
https://docs.djangoproject.com/en/5.0/howto/csrf/#using-csrf-protection-with-ajax
"""
@login_required(login_url = 'login')
@api_view(['DELETE'])
def delete_user(request, target_id):
    try:
        user = User.objects.get(id=target_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # check if you're admin
    if request.method == 'DELETE' and request.user.role == 'A':
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@login_required(login_url='login')
@api_view(['GET'])
def get_comment(request, task_id):
    
    # Get all the comment
    task = Task.objects.get(id = task_id)
    task_comment = Comment.objects.filter(taskToComment = task)

    serializer = GetCommentSerializer(task_comment, many = True)

    return Response(serializer.data)


@login_required(login_url = 'login')
@api_view(['POST'])
def post_comment(request, task_id):
    # get user
    task = Task.objects.get(id = task_id)

    serializer = CommentSerializer(data = request.data) 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Work for comment section, get comment and post comment 


        