from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Book(models.Model):
    COVER_CHOICES = ("HARD", "SOFT")
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    cover = models.CharField(choices=COVER_CHOICES, default="HARD")
    inventory = models.PositiveIntegerField()
    fee = models.DecimalField(max_digits=5, decimal_places=2)
