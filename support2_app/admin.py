from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html

from .models import *


class AgentAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_id', 'name', 'uniq', 'is_boss', 'is_permission', 'show_brand', 'created_at']
    list_editable = ['tg_id', 'name', 'uniq', 'is_boss', 'is_permission']
    search_fields = ['name', 'uniq', 'tg_id']
    list_per_page = 10


class ContractAdmin(admin.ModelAdmin):
    list_display = ['id', 'project', 'agent', 'inn', 'code', 'status']
    list_editable = ['status']
    search_fields = ['inn', 'code', 'agent__name', 'project__name']


class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand_link', 'name', 'created_at']
    list_editable = ['name']
    search_fields = ['name']

    def brand_link(self, obj):
        url = (
                reverse("admin:support2_app_brand_changelist")
                + f"?region__id__exact={obj.id}"
        )
        return format_html('<a href="{}">{}</a>', url, obj.id)

    brand_link.short_description = "Бренды"


class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'agent_link', 'name', 'uniq', 'created_at']
    list_editable = ['name', 'uniq']
    search_fields = ['name']

    def agent_link(self, obj):
        url = (
                reverse("admin:support2_app_agent_changelist")
                + f"?brand__id__exact={obj.id}"
        )
        return format_html('<a href="{}">{}</a>', url, obj.id)

    agent_link.short_description = "Агенты"


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'uniq', 'is_special', 'brand', 'file', 'created_at']
    list_editable = ['name', 'uniq', 'brand', 'is_special']
    search_fields = ['name', 'uniq']


class CounterAdmin(admin.ModelAdmin):
    list_display = ['id', 'count']
    list_editable = ['count']
    readonly_fields = ['year']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.unregister(Group)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Counter, CounterAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Contract, ContractAdmin)

admin.site.site_title = 'Support S'
admin.site.site_header = 'Support S'
