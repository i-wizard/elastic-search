import uuid
from django.db import models
from django.utils import timezone


def generate_id():
    return uuid.uuid4().hex

def update_object(obj, data):
    for key, value in data.items():
        setattr(obj, key, value)
    obj.save()
    return obj

class BaseQuerySet(models.QuerySet):
    def delete(self):
        return super(BaseQuerySet, self).update(deleted_at=timezone.now(), is_deleted=True)
    
    def alive(self):
        return self.filter(is_deleted=False)

class CustomManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive = kwargs.pop("alive_only", True)
        super(CustomManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive:
            return BaseQuerySet(self.model, using=self._db).alive()
        return BaseQuerySet(self.model, using=self._db)

class BaseAbstractModel(models.Model):
    """
    Base Abstract model
    All models on this project will inherit from this
    """

    id = models.CharField(
        max_length=255, primary_key=True, default=generate_id, editable=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = CustomManager()
    all_objects = CustomManager(alive_only=False)
    
    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def delete(self, soft_delete: bool = True):
        if soft_delete:
            self.deleted_at = timezone.now()
            self.is_deleted = True
            return self.save()