"""
Settings for the admin backend
"""

# Django
from django.contrib import admin

# AA Discord Announcements
from aa_discord_announcements.models import PingTarget, Webhook


@admin.register(PingTarget)
class PingTargetAdmin(admin.ModelAdmin):
    """
    DiscordPingTargetsAdmin
    """

    list_display = (
        "_name",
        "discord_id",
        "_restricted_to_group",
        "notes",
        "is_enabled",
    )

    filter_horizontal = ("restricted_to_group",)
    readonly_fields = ("discord_id",)
    ordering = ("name",)

    @classmethod
    @admin.display(description="Ping Target", ordering="name")
    def _name(cls, obj):
        return obj.name

    @classmethod
    @admin.display(description="Restricted to", ordering="restricted_to_group__name")
    def _restricted_to_group(cls, obj):
        names = [x.name for x in obj.restricted_to_group.all().order_by("name")]

        if names:
            return ", ".join(names)

        return None


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    """
    WebhookAdmin
    """

    list_display = ("_name", "_url", "_restricted_to_group", "notes", "is_enabled")

    filter_horizontal = ("restricted_to_group",)
    ordering = ("name",)

    @classmethod
    @admin.display(description="Channel Name", ordering="name")
    def _name(cls, obj):
        return obj.name

    @classmethod
    @admin.display(description="Webhook URL", ordering="url")
    def _url(cls, obj):
        return obj.url

    @classmethod
    @admin.display(description="Restricted to", ordering="restricted_to_group__name")
    def _restricted_to_group(cls, obj):
        names = [x.name for x in obj.restricted_to_group.all().order_by("name")]

        if names:
            return ", ".join(names)

        return None
