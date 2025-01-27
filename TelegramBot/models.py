from django.db import models

class TGUser(models.Model):
    user_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    sap_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
