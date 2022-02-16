from django.contrib import admin
from .models import Place, Image
from django.utils.safestring import mark_safe


class ImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ['preview_image']
    fields = ('image', 'preview_image', 'image_number')

    def preview_image(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 200px;">'
            )


class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]


admin.site.register(Place, PlaceAdmin)
admin.site.register(Image)
