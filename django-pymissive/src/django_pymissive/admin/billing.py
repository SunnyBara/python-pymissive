"""Admin for MissiveBilling model."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from django_boosted import AdminBoostModel
from ..models.billing import MissiveBilling


class MissiveBillingInline(admin.TabularInline):
    """Inline for billing records on missive."""

    model = MissiveBilling
    extra = 0
    readonly_fields = ["created_at"]
    fields = ["recipient", "billing_amount", "estimate_amount", "currency", "is_billed", "invoice", "created_at"]
    raw_id_fields = ["recipient"]
    can_delete = True
    show_change_link = True
    readonly_fields = [
        "missive",
        "recipient",
        "billing_amount",
        "estimate_amount",
        "currency",
        "is_billed",
        "invoice",
        "created_at",
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(MissiveBilling)
class MissiveBillingAdmin(AdminBoostModel):
    """Admin for billing records."""

    list_display = [
        "missive",
        "recipient",
        "billing_amount",
        "estimate_amount",
        "is_billed",
        "created_at",
    ]
    list_filter = [
        "missive__provider",
        "missive__missive_type",
        "is_billed"
    ]
    search_fields = [
        "missive__external_id",
        "missive__subject",
        "recipient__name",
        "recipient__email",
        "recipient__phone",
    ]
    raw_id_fields = ["missive", "recipient"]
    readonly_fields = ["created_at", "updated_at"]
    actions = ["set_billed"]

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "missive",
                    "recipient",
                    "billing_amount",
                    "estimate_amount",
                    "currency",
                    "invoice",
                    "is_billed",
                )
            },
        ),
    ]
    def change_fieldsets(self):
        """Configure fieldsets for change view."""
        self.add_to_fieldset(_("Comment/Timestamps"), ["comment", "created_at", "updated_at"])

    @admin.action(description=_("Mark as billed"))
    def set_billed(self, request, queryset):
        updated = queryset.filter(billing_amount__gt=0).update(is_billed=True)
        self.message_user(request, _(f"{updated} record(s) marked as billed."))
