from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

    class Meta:
        db_table = "Notes"
        # default_permissions = ()

    def __str__(self):
        return self.name

class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='shared_notes')
    shared_with = models.ManyToManyField(User)

    class Meta:
        db_table = "ShareNotes"
        # default_permissions = ()

class Version(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Versions"
        # default_permissions = ()
