from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models



# Create user 
class CustomUser(AbstractUser):
    """
    This model should have permission.  
    """
    pass

class Mission(models.Model):
    name = models.CharField(max_length = 100)
    detail = models.TextField(verbose_name="Details", blank = True, null = True)
    createBy = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = 'mission_owner')
    createTime = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name #  to be done


class Drawing(models.Model):
    name = models.CharField(max_length=100)
    mission = models.ForeignKey(Mission, on_delete = models.CASCADE, related_name= "drawing_in_mission")
    geom = gis_models.GeometryField(blank=True)
    properties = models.JSONField(blank = True, null = True)

    def __str__(self):
        return self.name