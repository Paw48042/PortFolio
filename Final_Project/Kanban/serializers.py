from rest_framework import serializers 
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','taskName', 'detail', 'createBy','assigned','status', 'createTime']
        depth = 2
        
        def get_createTime(self, obj):
            return obj.createTime.strftime("%b %d %Y, %I:%M %p")
        def update(self, instance, validated_data):
            instance.status = validated_data.get('status', instance.status)
            instance.save()
            return instance

class CreateTaskSerializer(serializers.ModelSerializer):
     class Meta:
        model = Task
        fields = ['id','taskName', 'detail', 'createBy','assigned','status', 'createTime']


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','username', 'email', 'role', 'company','profilePic','first_name','last_name']
        def update_role(self, instance, validated_data):
            instance.role = validated_data.get('role', instance.role)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author','taskToComment','createTime','comment']

class GetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','author','taskToComment','createTime','comment']
        depth = 1

class UpdateTaskSerializer(serializers.ModelSerializer): # For update progress
    class Meta:
        model = Task
        fields = ['status']

class EditTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['taskName','detail','assigned','status']

class UpdateRoleSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['role']

# another seializer for comment 
