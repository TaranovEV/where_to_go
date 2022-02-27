from django.contrib import admin
from .models import Place, Image
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    readonly_fields = ['preview_image']
    fields = ('image', 'preview_image', 'image_number')

    def preview_image(self, obj):
        return (
            format_html(
                mark_safe(
                    '<img src="{}" style="max-height: 200px;">'
                ),
                obj.image.url
            )
        )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]


admin.site.register(Image)
