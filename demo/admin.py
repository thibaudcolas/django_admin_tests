from django.apps import apps
from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.contenttypes.models import ContentType
from django.contrib.flatpages.models import FlatPage
from django.contrib.redirects.models import Redirect
from django.contrib.sessions.models import Session
from django.contrib.sites.models import Site
from django.contrib.flatpages.admin import FlatPageAdmin
from django.shortcuts import render
from django.urls import path
from django.utils.version import get_version

from demo.models import Artist, Release, ReleaseTrack, Track

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

admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Permission)
admin_site.register(LogEntry)
admin_site.register(FlatPage, FlatPageAdmin)
admin_site.register(Redirect)
admin_site.register(Session)
admin_site.register(Site)
admin_site.register(ContentType)


class ReleaseInline(admin.StackedInline):
    model = Release


class ReleaseTrackInline(admin.TabularInline):
    fields = ["track_number", "track"]
    model = ReleaseTrack


@admin.register(Artist, site=admin_site)
class ArtistAdmin(admin.ModelAdmin):
    inlines = [ReleaseInline]
    readonly_fields = ["id"]
    search_fields = ["name"]
    list_per_page = 100


@admin.register(Release, site=admin_site)
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


@admin.register(ReleaseTrack, site=admin_site)
class ReleaseTrackAdmin(admin.ModelAdmin):
    autocomplete_fields = ["release", "track"]
    search_fields = ["release__title", "track__title", "release__artist__name"]
    list_per_page = 100


@admin.register(Track, site=admin_site)
class TrackAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    search_fields = ["artists__name", "title"]
    list_per_page = 50
