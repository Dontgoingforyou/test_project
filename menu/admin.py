from django.contrib import admin

from menu.models import MenuItem, Menu


class MenuItemInLine(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('title', 'url', 'parent', 'order')
    ordering = ('order',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [MenuItemInLine]
