from django.db import models
from bbs.models import UserProfile


# Create your models here.
class WebGroup(models.Model):
    name = models.CharField(max_length=64)
    brief = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE)
    admins = models.ManyToManyField(UserProfile, related_name='group_admins')
    members = models.ManyToManyField(UserProfile, related_name='group_members', blank=True, null=True)
    max_members = models.IntegerField(default=200)
    def __str__(self):
        return self.name


