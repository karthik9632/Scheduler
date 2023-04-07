from django.db import models

# Create your models here.

class Statuses(object):
    RECEIVED, PROCESSING, SHIPPED, CLOSED = range(0, 4)

    CHOICES = (
        (RECEIVED, 'Received'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (CLOSED, 'Closed'),
    )


class Atadmin(models.Model):
    name=models.CharField(unique=True, max_length=20)
    status = models.IntegerField(
        choices=Statuses.CHOICES,
        default=Statuses.RECEIVED,
    )


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Atadmin, on_delete=models.CASCADE, related_name='authorname')