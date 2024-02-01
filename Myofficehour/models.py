from django.db import models

# Create your models here.
class Officehour(models.Model):
    when = models.DateTimeField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Location(models.Model):
    officehour = models.ForeignKey(
        "Officehour",
        on_delete=models.CASCADE,
    )
    location = models.CharField(null=False,blank=False,max_length=64)
    mapURL = models.TextField(null=True,blank=True,max_length=120)
    picture = models.FileField(upload_to="upload/%Y-%m-%d/",blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Status(models.Model):
    officehour = models.ForeignKey(
        "Officehour",
        on_delete=models.CASCADE,
    )
    STATUS_CHOICES = [
    ("OT","Ontime"),
    ("OC","Canceled"),
        ("DL","Delayed"),
        ("PP","Postponed"),
        ("ES","Early")
    ]
    status = models.CharField(choices=STATUS_CHOICES,null=True, blank=False,max_length=16, default="NA")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Participant(models.Model):
    officehour = models.ForeignKey(
        "Officehour",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=32)
    email = models.EmailField(null=False,blank=False)
    ip = models.GenericIPAddressField(null=False,blank=False)
    ua = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

