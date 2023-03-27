from django.contrib import admin
from django.contrib.auth.models import User, Group

from main.models import Menu, Item


class ItemInline(admin.StackedInline):
	model = Item
	extra = 1
	fields = ['title']
	verbose_name = 'Корневой пункт меню'
	verbose_name_plural = 'Корневые пункты меню'

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		return qs.filter(parent__isnull=True)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
	list_display = ['name']
	inlines = [ItemInline]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = ['title', 'parent']
	fields = ['parent', 'title']

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		return qs.filter(parent__isnull=False)


admin.site.unregister(User)
admin.site.unregister(Group)
