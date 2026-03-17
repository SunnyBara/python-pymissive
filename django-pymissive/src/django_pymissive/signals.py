"""Signal handlers for django_pymissive."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.event import MissiveEvent


@receiver(post_save, sender=MissiveEvent)
def trigger_billings_on_event(sender, instance, created, **kwargs):
    """Call get_billings on the missive after an event is saved."""
    if instance.missive_id and instance.missive.can_billings():
        instance.missive.get_billings()
