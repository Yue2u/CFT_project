from django.db import models

# Create your models here.


class ImageHolder(models.Model):
    image = models.ImageField(upload_to='images/')
    upload_date = models.DateTimeField(auto_now_add=True)
    user_ip = models.CharField(max_length=16, default='')
    id = models.IntegerField(primary_key=True)

# # 'log_id': self.id, 'user_ip': self.user.ip_v4,
# # 'uploaded_images': {'image_id': self.uploaded_images.id, 'upload_date': self.uploaded_images.upload_date}



