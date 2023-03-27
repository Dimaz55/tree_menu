from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from main.models import Item


@receiver(pre_save, sender=Item)
def item_pre_save(sender, instance, **kwargs):
	instance.root = instance.pk
	if not instance.menu_id:
		instance.menu = instance.parent.menu

	if instance.parent:
		instance.level = instance.parent.level + 1
		instance.root = instance.parent.root
	else:
		instance.level = 0


@receiver(post_save, sender=Item)
def item_post_save(sender, instance, **kwargs):
	if kwargs['created']:
		instance.root = instance.pk
		if instance.parent:
			instance.parent.has_children = True
			instance.parent.save()
		instance.save()
