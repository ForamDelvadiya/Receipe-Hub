from django.db import models
from  django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .utils import generate_slug

User = get_user_model()


# Create your models here.


class Receipe(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True , blank=True)
    receipe_name = models.CharField(max_length=100 , null=True)
    slug = models.SlugField(default='default-slug',unique=True)
    receipe_desc = models.TextField()
    receipe_img = models.ImageField(upload_to="receipe")
    receipe_view_count = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False) 
    
    def save(self , *args , **kwargs):
        self.slug = generate_slug(self.receipe_name)
        super(Receipe , self).save(*args , **kwargs)
