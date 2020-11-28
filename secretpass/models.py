from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    owner = models.ForeignKey(User, related_name="account", on_delete=models.CASCADE)
    service = models.CharField(max_length=30)
    username = models.CharField(max_length=50)
    password = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return (
            "["
            + self.owner.username
            + "] - "
            + self.service
            + " - "
            + self.username
            + " - "
            + self.password
        )
