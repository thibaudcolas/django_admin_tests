import os
import re
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
from django.contrib.staticfiles import finders
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
            path('styleguide/', self.styleguide, name='styleguide'),
        ]
        return custom_urls + urls

    def styleguide(self, request):
        messages.set_level(request, messages.DEBUG)

        message_types = {
            messages.DEBUG: {"color": "#70bf2b", "type": "debug"},
            messages.INFO: {"color": "#70bf2b", "type": "info"},
            messages.SUCCESS: {"color": "#70bf2b", "type": "success"},
            messages.WARNING: {"color": "#efb80b", "type": "warning"},
            messages.ERROR: {"color": "#dd4646", "type": "error"},
        }
        for level, msg in message_types.items():
            messages.add_message(request, level, f'This is a {msg["type"]} message <span style="color: {msg["color"]}; background-color: var(--message-{msg["type"]}-bg)">Contrast</span>.')

        icons = []
        for finder in finders.get_finders():
            for path, storage in finder.list([]):
                if path.endswith('.svg'):
                    with storage.open(path) as file:
                        svg = file.read().decode('utf-8')

                        icons.append({
                            "filename": os.path.basename(path)[:-4],
                            "path": path,
                            "contents": svg,
                            # Extract the first fill color from the SVG
                            "fill": re.search(r'fill="([^"]+)"', svg).group(1)
                        })

        # Redirect to the model's admin change list
        return render(request, "admin/styleguide.html", {
            "icons": icons,
            "has_permission": True,
        })



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
