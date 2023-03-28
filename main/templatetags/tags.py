from django import template

from main.models import Item

register = template.Library()


def build_menu(res, items, level, root, pk=None, parent_id=None, indent=0):
	for item in items:
		item_id = item['id']
		if item['parent'] == parent_id:
			if level + 1 >= item['level'] and root == item['root'] or not item['root'] or item['parent'] == pk:
				b_open = '<b>' if pk == item_id else ''
				b_close = '</b>' if pk == item_id else ''
				a_open = f'<a href="{str(item_id)}">'
				a_close = '</a>'
				indents = f'{"&nbsp"*indent}'
				res.append(f'{indents}{a_open}{b_open}{item["title"]}{b_close}{a_close}')
			build_menu(res, items, level, root, pk, item_id, indent + 2)
	return res


def get_item(items, value):
	if not value:
		return None
	for item in items:
		if item['id'] == value:
			return item


@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context, menu_name):
	menu_items = Item.objects. \
		select_related('menu'). \
		filter(menu__name=menu_name).\
		values('id', 'title', 'parent', 'root', 'level')

	pk = context.get('pk')
	items = list(menu_items)
	if pk and get_item(items, pk):
		item = get_item(items, pk)
		root = item.get('root')
		level = item.get('level')
	else:
		level = 1
		root = None
	res = []
	menu_tree = build_menu(res, items, level, root, pk)

	return {
		'menu': menu_tree,
		# Не показывать заголовок если меню не найдено
		'menu_name': menu_name if menu_items else ''
	}
