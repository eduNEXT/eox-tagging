"""
Admin class.
"""
from django.contrib import admin, messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey

from eox_tagging.forms import TagForm
from eox_tagging.models import Tag, OpaqueKeyProxyModel


class TagAdmin(admin.ModelAdmin):
    """Tag admin."""
    list_display = [
        "tag_type",
        "tag_value",
        "tagged_object",
        "owner",
        "status",
    ]
    readonly_fields = (
        'status',
        'invalidated_at',
    )
    search_fields = ('tag_type', 'tag_value', 'status')

    form = TagForm

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
        Displays useful info about the owner of the tag.
        """
        # pylint: disable=broad-except
        try:
            return u"{}: {}".format(tag.owner_object_type, tag.owner_object)
        except Exception as error:
            return str(error)

    def tagged_object(self, tag):
        """
        Displays useful info about the tagged object.
        """
        # pylint: disable=broad-except
        try:
            if tag.target_object:
                return u"{}: {}".format(tag.target_object_type, tag.target_object)
            return u"Resource locator: {}".format(tag.resource_locator)
        except Exception as error:
            return str(error)

    def add_view(self, request, *args, **kwargs):  # pylint: disable=arguments-differ
        """
        Custom method to handle the specific case of tagging course_keys
        """
        if request.POST:
            selected_object = request.POST['target_type'] and request.POST['target_object_id']

            # If is post request and there's only opaque key
            opaque_key_target = request.POST['opaque_key'] and not selected_object

            if opaque_key_target:

                try:
                    course_key = CourseKey.from_string(request.POST['opaque_key'])
                except InvalidKeyError:
                    message = u"EOX_TAGGING | Error: Opaque Key %s does not match with opaque_keys.edx definition." \
                              % request.POST['opaque_key']
                    messages.error(request, message)
                    return HttpResponseRedirect(request.path)

                _mutable = request.POST._mutable  # pylint: disable=protected-access
                request.POST._mutable = True  # pylint: disable=protected-access
                model_instance = OpaqueKeyProxyModel.objects.create(opaque_key=course_key)
                request.POST['target_type'] = ContentType.objects.get(model='OpaqueKeyProxyModel').id
                request.POST['target_object_id'] = model_instance.id
                request.POST._mutable = _mutable  # pylint: disable=protected-access

        return super(TagAdmin, self).add_view(request, *args, **kwargs)


admin.site.register(Tag, TagAdmin)
