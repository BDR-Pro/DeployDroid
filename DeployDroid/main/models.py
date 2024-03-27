from django.db import models

class ChocolateyPackage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    

    def __str__(self):
        return self.name
    