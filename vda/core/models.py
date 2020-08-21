from django.db import models

class Guestbook(models.Model):
    first_name = models.CharField(max_length=100)
    user_message = models.CharField(max_length = 300)
    pub_date = models.DateField()