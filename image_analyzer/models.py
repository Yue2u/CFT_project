from django.db import models

# Create your models here.


class ImageHolder(models.Model):
    image = models.ImageField(upload_to='images/')
    user_ip = models.CharField(max_length=16, default='')
    image_path = models.CharField(max_length=200, default='')
    upload_date = models.DateTimeField(auto_now_add=True)
    id = models.IntegerField(primary_key=True)

