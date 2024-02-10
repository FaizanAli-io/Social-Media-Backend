import uuid

from django.db import models


class Hashtag(models.Model):

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Attributes
    content = models.CharField(max_length=50)
    occurrence = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'#{self.content} - {self.occurrence}'

    class Meta:
        ordering = ['-occurrence']
