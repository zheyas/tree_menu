
from django import template
from ..models import MenuItem

register = template.Library()

def build_tree(items, parent=None):
    tree = []
    for item in items:
        if item.parent_id == (parent.id if parent else None):
            children = build_tree(items, item)
            tree.append({
                'item': item,
                'children': children,
                'active': False,
                'active_path': False,
                'show_children': False
            })
    return tree

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    # Один-единственный запрос к MenuItem!
    items = list(MenuItem.objects.filter(menu__name=menu_name).select_related('parent'))
    tree = build_tree(items)
    path = context['request'].path

    def mark_active(nodes, level=0):
        found = False
        for node in nodes:
            url = node['item'].get_url()
            if url == path or path.rstrip('/') == url.rstrip('/'):
                node['active'] = True
                node['active_path'] = True
                node['show_children'] = True
                found = True
            elif mark_active(node['children'], level+1):
                node['active_path'] = True
                node['show_children'] = True
                found = True
        return found

    mark_active(tree)
    return {'tree': tree, 'request': context['request']}
