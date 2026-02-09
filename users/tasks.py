from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta


@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    one_month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True
    )

    inactive_users.update(is_active=False)

    return f"Deactivated {inactive_users.count()} users"
