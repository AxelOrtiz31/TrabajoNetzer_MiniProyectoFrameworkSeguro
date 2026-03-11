from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class Task(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5, "El título debe tener al menos 5 caracteres.")])
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title