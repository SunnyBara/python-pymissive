from django.utils import timezone

from ..models.campaign import MissiveScheduledCampaign


def run_campaign(campaign_id):
    scheduled = MissiveScheduledCampaign.objects.get(
        id=campaign_id, send_date__isnull=True
    )
    scheduled.send_date = timezone.now()
    scheduled.save()
    try:
        scheduled.run_campaign()
    finally:
        # Clear processing flag so campaign can be restarted if needed
        campaign = scheduled.campaign
        metadata = dict(campaign.metadata or {})
        metadata.pop("processing", None)
        campaign.metadata = metadata
        campaign.save(update_fields=["metadata"])
    scheduled.ended_at = timezone.now()
    scheduled.save()
