from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    # user that owns this tag
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

# represents a physical container within which parts will be stored.
class Container(models.Model):
    # user that owns this container
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user-friendly name for the container
    name = models.CharField(max_length=128)
    description = models.TextField()
    # regex describing a valid naming scheme for locations in this container
    naming_scheme = models.CharField(max_length=128)

    def __str__(self):
        return self.name

# represents a physical part
class Part(models.Model):
    # user with which the part is associated
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # user-friendly name of the part
    name = models.CharField(max_length=50)
    # slug generated from the name, should be unique within the user's parts
    slug = models.SlugField(blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    description = models.TextField(blank=True)
    datasheet = models.FileField(blank=True)
    pinout = models.ImageField(blank=True)

    quantity = models.PositiveSmallIntegerField(default=0)
    price = models.DecimalField(blank=True, null=True,
                                max_digits=10, decimal_places=2)

    container = models.ForeignKey(Container, on_delete=models.PROTECT)
    # this location should be verified against the relevant container's naming
    # scheme
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name
