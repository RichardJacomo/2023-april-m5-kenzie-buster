from django.db import models
from users.models import User


class Rating(models.TextChoices):
    G = "G"
    PG = "PG"
    PG13 = "PG-13"
    R = "R"
    NC17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, null=True, default=None)
    rating = models.CharField(
        max_length=20,
        choices=Rating.choices,
        default=Rating.G,
        null=True,
    )
    synopsis = models.TextField(null=True, default=None)
    order = models.ManyToManyField(
        User, through="MovieOrder", related_name="movie_orders")

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="movies")


class MovieOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    buyed_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)