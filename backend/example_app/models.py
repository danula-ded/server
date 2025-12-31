from django.db import models

from common.models import TimestampedModel


class ExampleItem(TimestampedModel):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
