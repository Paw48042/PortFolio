from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.utils import timezone

def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.username}/{filename}'

# Create your models here.

class User(AbstractUser):
    role_choices = {
        'A':'Administrator',
        'M':'Member'
    }
    role = models.CharField(max_length = 1,choices = role_choices, default = 'M')
    company = models.CharField(max_length = 255)
    profilePic = models.ImageField(upload_to= user_directory_path, default='default.jpg' )
    class Meta:
        permissions = [
            ('CreateTeam', 'Be able to create Team'),
            ('UpdateTeam', 'Be able to update Team'),
            ('DeleteTeam', 'Be able to delete Team'),
            ('CreateTask', 'Be able to create task'),
            ('UpdateTask', 'Be able to update task'),
            ('DeleteTask', 'Be able to delete task'),
            ('CreateSubTask', 'Be able to create subtask'),
            ('UpdateSubTask', 'Be able to update subtask'),
            ('DeleteSubTask', 'Be able to Delete subtask'),
        ]
    def __str__(self):
        return f"username = {self.username}, email = {self.email}, company = {self.company}, role = {self.role}"

class Task(models.Model):
    taskName = models.CharField(max_length = 255, blank = False)
    detail = models.TextField(blank = True)
    createBy = models.ForeignKey(User, on_delete = models.PROTECT, related_name = "Creator")
    createTime = models.DateTimeField(auto_now_add = True)
    assigned = models.ManyToManyField(User, related_name = "assigned")

    # Define the status choices
    statusChoices = {
        'T' : 'To Do',
        'P' : 'Processing',
        'F' : 'Finished'
    }

    status = models.CharField(max_length = 1,choices = statusChoices, default = "T")
    def __str__(self):
        return f"{self.taskName} - Created at {self.createTime.strftime('%b %d %Y, %I:%M %p')}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete = models.PROTECT, related_name = "author")
    taskToComment = models.ForeignKey(Task, on_delete = models.CASCADE, related_name = "task_commented")
    comment = models.TextField(blank = True)
    createTime =  models.DateTimeField(auto_now_add = True)
