from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    COVER_CHOICES = (
        ("HARD", "Hard Cover"),
        ("SOFT", "Soft Cover")
    )
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    cover = models.CharField(max_length=4, choices=COVER_CHOICES, default="HARD")
    inventory = models.PositiveIntegerField()
    fee = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
