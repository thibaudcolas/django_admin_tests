from django.apps import apps
from django.contrib import admin, messages
from django.shortcuts import render
from django.urls import path
from django.utils.version import get_version

from demo.models import Artist, Release, ReleaseTrack, Track


class ReleaseInline(admin.StackedInline):
    model = Release


class ReleaseTrackInline(admin.TabularInline):
    fields = ["track_number", "track"]
    model = ReleaseTrack


class ArtistAdmin(admin.ModelAdmin):
    inlines = [ReleaseInline]
    readonly_fields = ["id"]
    search_fields = ["name"]
    list_per_page = 100


class ReleaseAdmin(admin.ModelAdmin):
    autocomplete_fields = ["artist"]
    date_hierarchy = "release_date"
    inlines = [ReleaseTrackInline]
    list_display = ["title", "artist", "type", "release_date"]
    list_editable = ["type", "release_date"]
    list_filter = ["type"]
    readonly_fields = ["id"]
    search_fields = ["title", "artist__name"]
    list_per_page = 100


class ReleaseTrackAdmin(admin.ModelAdmin):
    autocomplete_fields = ["release", "track"]
    search_fields = ["release__title", "track__title", "release__artist__name"]
    list_per_page = 100


class TrackAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    search_fields = ["artists__name", "title"]
    list_per_page = 50


class MyAdminSite(admin.AdminSite):
    site_header = f"Django administration {get_version()}"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('test_messages/', self.test_messages, name='test_messages'),
        ]
        return custom_urls + urls

    def test_messages(self, request):
        # Here we trigger one message of each type
        messages.add_message(request, messages.DEBUG, 'This is a debug message.')
        messages.add_message(request, messages.INFO, 'This is an info message.')
        messages.add_message(request, messages.SUCCESS, 'This is a success message.')
        messages.add_message(request, messages.WARNING, 'This is a warning message.')
        messages.add_message(request, messages.ERROR, 'This is an error message.')

        # Redirect to the model's admin change list
        return render(request, "admin/test_messages.html", {})


admin_site = MyAdminSite(name="myadmin")
models = apps.get_models()

for model in models:
    try:
        admin_site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
