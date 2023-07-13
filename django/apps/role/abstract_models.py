from django.db import models
from django.conf import settings

from libs.db.models.abstract_models import AbstractModels
from libs.db.models.fields import JSONField


class AbstractRole(AbstractModels):
    name = models.CharField(max_length=16)
    permissions = models.JSONField()
    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='roles'
    )
    class Meta:
        abstract = True
