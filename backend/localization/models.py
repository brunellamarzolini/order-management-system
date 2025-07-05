from django.db import models

class Language(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name