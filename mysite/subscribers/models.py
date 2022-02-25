from django.db import models


class Subscriber(models.Model):
    email = models.CharField(max_length=50, blank=False, null=False, help_text="Email address")
    name = models.CharField(max_length=150, blank=False, null=False, help_text="Enter you name")


    def __str__(self):
        return self.name