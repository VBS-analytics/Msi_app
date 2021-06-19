from django.db import models

# Create your models here.

class MsiFilters(models.Model):
    filter_name = models.CharField(max_length=120)
    filter_date = models.DateTimeField(auto_now=True)
    filter_data = models.TextField()

    def __str__(self):
        return self.filter_name