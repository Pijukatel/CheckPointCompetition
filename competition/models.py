from django.db import models

# Create your models here.


class CheckPoint(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField()
    gps_lat = models.FloatField()
    gps_lon = models.FloatField()
    photo = models.ImageField(upload_to='checkpoints')
