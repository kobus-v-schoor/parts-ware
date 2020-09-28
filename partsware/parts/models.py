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
    description = models.TextField(blank=True)
    # regex describing a valid naming scheme for locations in this container
    naming_scheme = models.CharField(max_length=128)

    def __str__(self):
        return self.name

def datasheet_upload_to(instance, filename):
    return f'{instance.user.id}/datasheets/{filename}'

def pinout_upload_to(instance, filename):
    return f'{instance.user.id}/pinouts/{filename}'

def image_upload_to(instance, filename):
    return f'{instance.user.id}/images/{filename}'

# represents a physical part
class Part(models.Model):
    # user with which the part is associated
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # user-friendly name of the part
    name = models.CharField(max_length=50)

    tags = models.ManyToManyField(Tag, blank=True)

    description = models.TextField(blank=True)

    image = models.ImageField(blank=True, upload_to=image_upload_to)
    datasheet = models.FileField(blank=True, upload_to=datasheet_upload_to)
    pinout = models.ImageField(blank=True, upload_to=pinout_upload_to)

    quantity = models.PositiveSmallIntegerField(default=0)
    price = models.DecimalField(blank=True, null=True,
                                max_digits=10, decimal_places=2)

    container = models.ForeignKey(Container, on_delete=models.PROTECT)
    # this location should be verified against the relevant container's naming
    # scheme
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name
