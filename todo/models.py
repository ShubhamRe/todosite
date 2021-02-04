from django.db import models
from django.contrib.auth.models import User

# To decide how should our model(i.e under admin the page which looks like database) looks like which fields we need there and
# which fields will be readonly or null value acceptable etc.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True,blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # to map user id with the todos created by that user.

    def __str__(self):
        return self.title
