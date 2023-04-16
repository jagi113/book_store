from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
import uuid

# Create your models here.


class Book(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    slug = models.SlugField(default="", max_length=400, db_index=True, editable=False)
    title = models.CharField(max_length=400)
    author = models.CharField(max_length=2000, default="neuvedený")
    url = models.CharField(max_length=800)
    image = models.CharField(max_length=800, blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=now(), blank=True, null=True)
    updated_at = models.DateTimeField(default=now(), blank=True, null=True)

    class Meta:
        unique_together = (
            "slug",
            "author",
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.updated_at = now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"<<{self.title} -- {self.author}>>"
