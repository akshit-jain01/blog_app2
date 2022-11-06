from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class HomeModel(models.Model):
    uid = models.UUIDField(primary_key = True, editable=False, default=uuid.uuid4())
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add = True)

    class Meta:
        abstract = True

class Blog(HomeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length = 500)
    category = models.CharField(max_length = 255)
    description = models.TextField()
    cover = models.ImageField(upload_to="blogs")
    author_name = models.CharField(max_length = 255)
    createdAt = models.DateField(auto_now = True)

    def __str__(self) -> str:
        return self.title