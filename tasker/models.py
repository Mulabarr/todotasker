from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class Task(models.Model):
    main_task = models.CharField(max_length=255)
    end_date = models.DateField(default=None)
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='tasks'
    )
