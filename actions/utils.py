from django.contrib.contenttypes.models import ContentType
from .models import Action
import datetime
from django.utils import timezone

def create_action(user, act, target=None):
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user=user, act=act, created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct, target_id=target.id)
    if not similar_actions:
        action = Action(user=user, act=act, target=target)
        action.save()
        return True
    return False