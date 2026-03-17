"""Billing handling: fetch via provider.get_billings_{missive_type}, then process each billing."""
from .models.provider import MissiveProviderModel
from .models.billing import MissiveBilling
from .models.missive import Missive
from .utils import get_recipient


def _process_billing(missive, bill):
    lookup = {
        "missive": missive,
        "invoice": bill.get("invoice"),
        "billing_amount": bill.get("billing_amount"),
        "estimate_amount": bill.get("estimate_amount"),
    }
    if bill.get("recipient"):
        lookup["recipient"] = get_recipient(missive, bill.get("recipient"))
    defaults = {
        "currency": bill.get("currency"),
        "trace": bill.get("raw") or {},
    }
    MissiveBilling.objects.update_or_create(defaults=defaults, **lookup)


def handle_billings(**kwargs) -> None:
    """Fetch billings from provider and process each one."""
    provider = kwargs.get('provider')
    provider = MissiveProviderModel.objects.get(name=provider)
    service_name = f"get_billings_{kwargs.get('missive_type')}"
    if not hasattr(provider._provider, service_name):
        return
    billings = provider._provider.call_service_formatted(
        service_name, **kwargs
    )
    if not billings:
        return
    external_id = kwargs.get('external_id')
    try:
        missive = Missive.objects.get(external_id=external_id)
    except Missive.DoesNotExist:
        return
    for bill in billings:
        _process_billing(missive, bill)
