from django import template
from main.models import Item
register = template.Library()


@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context, menu_name):
    menu_items = Item.objects.\
        select_related('menu').\
        filter(menu__name=menu_name)

    item = menu_items.filter(pk=context['pk']).first()
    root = item.root if item else None

    # Если пункт меню ещё не выбран - показывать только корневые пункты
    level = item.level if item else 0

    return {
        'menu_items': menu_items.filter(parent__menu__isnull=True),
        # Не показывать заголовок если меню не найдено
        'menu_name': menu_name if menu_items else '',
        'item': item,
        'level': level,
        'root': root
    }
