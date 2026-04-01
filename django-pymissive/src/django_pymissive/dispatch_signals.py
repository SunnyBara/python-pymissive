"""Custom dispatch signals for Missive (subscribe via django.dispatch.receiver).

Duplicate (see Missive.duplicate_missive):
- missive_pre_duplicate: source_missive, resend, thread_type, thread_id
- missive_post_duplicate: source_missive, new_missive, resend

Send (see Missive.send_missive):
- missive_pre_send / missive_post_send: missive (the row being sent), old_missive
  (None for a first send; the previous HISTORY missive when sending a resend duplicate).
"""

from django.dispatch import Signal

missive_pre_duplicate = Signal()
missive_post_duplicate = Signal()

missive_pre_send = Signal()
missive_post_send = Signal()
