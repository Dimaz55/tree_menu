from django.db import models


class Menu(models.Model):
	name = models.CharField('Название меню', max_length=100)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Меню'
		verbose_name_plural = 'Меню'


class Item(models.Model):
	menu = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name='Меню')
	title = models.CharField('Название пункта', max_length=100)
	parent = models.ForeignKey(
		'self',
		on_delete=models.CASCADE,
		null=True, blank=True,
		related_name='children',
		verbose_name='Родительский пункт меню'
	)
	level = models.IntegerField(default=0, editable=False)
	root = models.IntegerField(null=True, editable=False)

	def __str__(self):
		return f'{self.title} ({self.menu.name})'

	class Meta:
		verbose_name = 'Пункт меню'
		verbose_name_plural = 'Пункты меню'
