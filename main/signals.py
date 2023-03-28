from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from main.models import Item


@receiver(pre_save, sender=Item)
def item_pre_save(sender, instance, **kwargs):
	if not instance.menu_id:
		instance.menu = instance.parent.menu

	if instance.parent:
		instance.level = instance.parent.level + 1
		instance.root = instance.parent.root if instance.parent.root else instance.parent.pk
	else:
		instance.level = 0

