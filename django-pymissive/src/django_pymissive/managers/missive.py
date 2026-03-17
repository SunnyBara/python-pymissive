from django.db import models
from django.db.models.expressions import Subquery, OuterRef
from django.db.models import F, Max, Q, Sum
from django.db.models.functions import Coalesce

from ..models.choices import (
    MissiveThreadType,
    MissiveStatus,
)


class BaseMissiveManager(models.Manager):
    """Manager for the Missive model."""

    def last_event_subquery(self, field: str = "event"):
        from ..models.event import MissiveEvent

        return Subquery(
            MissiveEvent.objects.filter(
                missive=OuterRef("pk"),
            )
            .order_by("-occurred_at", "-id")
            .values(field)[:1],
            output_field=models.CharField(),
        )

    def last_scheduled_subquery(self, field: str = "event"):
        from ..models.campaign import MissiveScheduledCampaign

        return Subquery(
            MissiveScheduledCampaign.objects.filter(
                campaign=OuterRef("campaign_id"),
                send_date__isnull=False,
            )
            .order_by(f"-{field}", "-id")
            .values(field)[:1],
            output_field=models.CharField(),
        )

    def is_billable_expr(self):
        return models.Case(
            models.When(total_billing_amount__gt=0, then=True),
            default=False,
            output_field=models.BooleanField(),
        )

    def is_billed_expr(self):
        return models.Case(
            models.When(
                Q(total_billing_amount__gt=0)
                & Q(total_billing_amount=F("total_billed_amount")),
                then=True,
            ),
            default=False,
            output_field=models.BooleanField(),
        )

    def total_billing_expr(self, field: str, is_billed: bool = False):
        from ..models.billing import MissiveBilling
        q_billed = Q(is_billed=True, missive_id=OuterRef("id")) if is_billed else Q(missive_id=OuterRef("id"))
        return Subquery(
            MissiveBilling.objects.filter(q_billed)
            .order_by()
            .values("missive_id")
            .annotate(total=Sum(field))
            .values("total")[:1],
            output_field=models.DecimalField(max_digits=10, decimal_places=4),
        )

    def get_queryset_annotated(self):
        qs = super().get_queryset()
        qs = qs.select_related("campaign")
        qs = qs.prefetch_related(
            "to_missiverecipient",
            "to_missiveattachment",
            "to_missiveevent",
            "to_missivebilling",
            "to_missiverelatedobject",
        )
        qs = qs.annotate(
            last_campaign_send_date=self.last_scheduled_subquery("send_date"),
            last_campaign_ended_at=self.last_scheduled_subquery("ended_at"),
            count_recipient=models.Count("to_missiverecipient", distinct=True),
            count_event=models.Count("to_missiveevent", distinct=True),
            last_event=self.last_event_subquery(field="event"),
            last_event_reason=self.last_event_subquery(field="reason"),
            last_event_date=Coalesce(Max("to_missiveevent__occurred_at"), F("created_at")),
            count_related_object=models.Count("to_missiverelatedobject", distinct=True),
            count_attachment=models.Count("to_missiveattachment", distinct=True),
            total_billing_amount=self.total_billing_expr("billing_amount"),
            total_estimate_amount=self.total_billing_expr("estimate_amount"),
            total_billed_amount=self.total_billing_expr("billing_amount", is_billed=True),
            **{
                f"count_recipient_{status.value.lower()}": models.Count(
                    "to_missiverecipient",
                    distinct=True,
                    filter=Q(to_missiverecipient__status=status),
                )
                for status in MissiveStatus
            },
        )
        qs = qs.annotate(
            is_billable=self.is_billable_expr(),
            is_billed=self.is_billed_expr(),
        )
        return qs


class MissiveManager(BaseMissiveManager):
    """Manager for the Missive model."""


    def count_missive_thread(self, thread_type: MissiveThreadType):
        qs = self.model._base_manager.get_queryset().filter(
            thread_type=thread_type, thread_id=OuterRef("thread_id")
        )
        return Subquery(
            qs.values("thread_id").annotate(count=models.Count("id")).values("count"),
            output_field=models.IntegerField(),
        )

    def get_queryset(self):
        qs = super().get_queryset_annotated()
        qs = qs.annotate(
            count_history=self.count_missive_thread(thread_type=MissiveThreadType.HISTORY),
            count_message=self.count_missive_thread(thread_type=MissiveThreadType.MESSAGE),
        )
        return qs


class MissiveHistoryManager(BaseMissiveManager):
    """Manager for the MissiveHistory model."""

    def get_queryset(self):
        qs = super().get_queryset_annotated()
        qs = qs.filter(thread_type=MissiveThreadType.HISTORY)
        return qs


class MissiveMessageManager(BaseMissiveManager):
    """Manager for the MissiveMessage model."""

    def get_queryset(self):
        qs = super().get_queryset_annotated()
        qs = qs.select_related("message_by")
        qs = qs.filter(thread_type=MissiveThreadType.MESSAGE)
        return qs