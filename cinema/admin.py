from django.contrib import admin
from django.utils.safestring import mark_safe

from cinema.models import *
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())  # указывем имя поля как в нашей модели

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Категории
    """
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Reviews
    extra = 1
    #readonly_fields = ("name", "email")


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    #readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    form = MovieAdminForm
    # readonly_fields = ("get_image",)
    # fieldsets = (
    #     (None, {
    #         "fields": (("title", "tagline"),)
    #     }),
    #     (None, {
    #         "fields": ("description", ("poster", "get_image"))
    #     }),
    #     (None, {
    #         "fields": ("year", ("world_premiere", "country"))
    #     }),
    #     ("Actors", {
    #         "classes": ("collapse",),
    #         "fields": (("actors", "directors", "genres", "category"),)
    #     }),
    #     (None, {
    #         "fields": (("budget", "fees_in_usa", "poster", "get_image"),)
    #     }),
    # )


admin.site.register(MovieShots)
admin.site.register(ActorDirector)
admin.site.register(Genre)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Reviews)
