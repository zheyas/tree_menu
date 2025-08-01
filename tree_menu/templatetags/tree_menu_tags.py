from django import template
from django.urls import resolve
from ..models import Menu

register = template.Library()

def build_tree(items, parent=None):
    tree = []
    for item in items:
        if item.parent_id == (parent.id if parent else None):
            children = build_tree(items, item)
            tree.append({
                'item': item,
                'children': children,
                'active': False,       # сам активен?
                'active_path': False,  # кто-то из потомков или сам активен?
                'show_children': False # нужно ли показывать детей?
            })
    return tree

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    menu = Menu.objects.prefetch_related('items').get(name=menu_name)
    items = list(menu.items.all())
    tree = build_tree(items)
    path = context['request'].path

    def mark_active(nodes, level=0):
        found = False
        for node in nodes:
            # Активный пункт
            if node['item'].get_url() == path:
                node['active'] = True
                node['active_path'] = True
                node['show_children'] = True  # Первый уровень под активным развёрнут
                found = True
            # Рекурсия по детям
            elif mark_active(node['children'], level+1):
                node['active_path'] = True # кто-то из детей - активный путь
                node['show_children'] = True # раскрываем эту ветку
                found = True
        return found

    mark_active(tree)
    return {'tree': tree, 'request': context['request']}
