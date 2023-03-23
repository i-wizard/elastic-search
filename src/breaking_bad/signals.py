from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from elasticsearch_dsl import Index
from .documents import CharacterIndex
from .models import Character

@receiver(post_save, sender=Character)
def index_product(sender, instance, **kwargs):
    chracter = CharacterIndex(meta={'id': instance.id}, **instance.__dict__)
    chracter.save()

@receiver(post_delete, sender=Character)
def delete_product(sender, instance, **kwargs):
    chracter = CharacterIndex(meta={'id': instance.id})
    chracter.delete()