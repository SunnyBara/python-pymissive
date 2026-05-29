"""Smoke tests for the Django integration."""

from django.apps import apps


def test_django_pymissive_app_loads():
    assert apps.is_installed("django_pymissive")
    assert apps.get_model("django_pymissive", "Missive")
