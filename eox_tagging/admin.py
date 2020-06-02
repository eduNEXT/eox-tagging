"""
Admin class
"""

from django.contrib import admin

from eox_tagging.models import Tag


class TagAdmin(admin.ModelAdmin):
    """Tag admin
    """

    list_display = [
        "tag_type",
        "tag_value",
        "tagged_object_name",
        "belongs_to_object_name"
    ]


admin.site.register(Tag, TagAdmin)
