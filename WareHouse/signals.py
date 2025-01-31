from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

from Lib.serializations import model_to_dict
from WareHouse.models import Warehouse, Shelf, Product, Inventory, InventoryItem
from SyncModule.models import ChangeLog

app_label = 'WareHouse'

@receiver(post_save, sender=Warehouse)
@receiver(post_save, sender=Shelf)
@receiver(post_save, sender=Product)
@receiver(post_save, sender=Inventory)
@receiver(post_save, sender=InventoryItem)
def log_change(sender, instance, created, **kwargs):
    if getattr(instance, '_is_local_sync', False):
        return

    change_type = 'insert' if created else 'update'
    new_state = model_to_dict(instance)
    ChangeLog.objects.create(
        app_label=app_label,
        model_name=sender.__name__,
        record_id=instance.id,
        change_type=change_type,
        new_state=new_state
    )

@receiver(post_delete, sender=Warehouse)
@receiver(post_delete, sender=Shelf)
@receiver(post_delete, sender=Product)
@receiver(post_delete, sender=Inventory)
@receiver(post_delete, sender=InventoryItem)
def log_delete(sender, instance, **kwargs):
    if getattr(instance, '_is_local_sync', False):
        return

    ChangeLog.objects.create(
        app_label=app_label,
        model_name=sender.__name__,
        record_id=instance.id,
        change_type='delete',
        new_state={}
    )

@receiver(m2m_changed, sender=InventoryItem.accommodations.through)
def log_m2m_change(sender, instance, action, **kwargs):
    if getattr(instance, '_is_local_sync', False):
        return

    if action in ["post_add", "post_remove", "post_clear"]:
        new_state = model_to_dict(instance)
        ChangeLog.objects.create(
        app_label=app_label,
            model_name=InventoryItem.__name__,
            record_id=instance.id,
            change_type='update',
            new_state=new_state
        )
