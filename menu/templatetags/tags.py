from django import template
from django.db.models import Prefetch
from django.urls import reverse, NoReverseMatch
from django.utils.safestring import mark_safe

from menu.models import Menu, MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):

    # Получение текущего URL
    try:
        request = context['request']
        current_path = request.path
        resolver_match = request.resolver_match
        current_url_name = resolver_match.url_name if resolver_match else ''
    except KeyError:
        current_url_name = ''

    # Получение меню и его элементов
    try:
        menu = Menu.objects.prefetch_related(
            Prefetch('items', queryset=MenuItem.objects.select_related('parent').order_by('order'))
        ).get(name=menu_name)
    except Menu.DoesNotExist:
        return ''

    # Формирование иерархии меню
    items = menu.items.all()

    menu_dict = {}
    for item in items:
        menu_dict[item.id] = {'item': item, 'children': []}

    root = []
    for item in items:
        if item.parent_id:
            parent = menu_dict.get(item.parent_id)
            if parent:
                parent['children'].append(menu_dict[item.id])
        else:
            root.append(menu_dict[item.id])

    # Определение активных пунктов меню
    active_ids = set()
    for item in items:
        if item.url.startswith('/'):
            item_url = item.url
        else:
            try:
                item_url = reverse(item.url)
            except NoReverseMatch:
                item_url = item.url

        if item_url == current_path:
            active = item
            while active:
                active_ids.add(active.id)
                active = active.parent

    def render_menu(nodes, depth=0):
        if not nodes:
            return ''
        indent = '  ' * depth
        html = f'{indent}<ul>\n'
        for node in nodes:
            item = node['item']
            is_active = item.id in active_ids
            has_children = len(node['children']) > 0
            css_classes = []
            if is_active:
                css_classes.append('active')
            if has_children and (is_active or depth < 1):
                css_classes.append('expanded')
            class_attr = f' class="{" ".join(css_classes)}"' if css_classes else ''
            html += f'{indent}  <li{class_attr}>\n'
            html += f'{indent}    <a href="{item.get_url()}">{item.title}</a>\n'
            if has_children and (is_active or depth < 1):
                html += render_menu(node['children'], depth + 1)
            html += f'{indent}  </li>\n'
        html += f'{indent}</ul>\n'
        return html

    return mark_safe(render_menu(root))
