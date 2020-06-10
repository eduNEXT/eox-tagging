"""
Admin class.
"""
from django.contrib import admin

from eox_tagging.models import Tag


class TagAdmin(admin.ModelAdmin):
    """Tag admin."""
    list_display = [
        "tag_type",
        "tag_value",
        "tagged_object",
        "owner",
    ]
    # search_fields = ('tag_type', 'tag_value', 'tagged_object', 'belongs_to')
    search_fields = ('tag_type', 'tag_value')

    def get_search_results(self, request, queryset, search_term):
        """
        Custom search to support searching on the tagged objects
        """
        queryset, use_distinct = super(TagAdmin, self).get_search_results(
            request,
            queryset,
            search_term
        )
        # TODO: we need to connect the TagQuery search here.
        return queryset, use_distinct

    def owner(self, tag):
        """
        Displays useful info about the owner of the tag
        """
        # pylint: disable=broad-except
        try:
            return u"{}: {}".format(tag.owner_object_name, tag.owner_object)
        except Exception as error:
            return str(error)

    def tagged_object(self, tag):
        """
        Displays useful info about the tagged object
        """
        # pylint: disable=broad-except
        try:
            return u"{}: {}".format(tag.target_object_name, tag.target_object)
        except Exception as error:
            return str(error)


admin.site.register(Tag, TagAdmin)
