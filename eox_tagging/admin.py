"""
Admin class
"""

from django.contrib import admin

from eox_tagging.models import Tag


class TagAdmin(admin.ModelAdmin):
    """Tag admin
    """
    pass


admin.site.register(Tag, TagAdmin)
