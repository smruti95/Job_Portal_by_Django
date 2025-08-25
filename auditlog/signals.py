from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.db import transaction
from .models import AuditLog
from .kafka_producer import publish_audit_log 
from .middleware import get_current_user  

@receiver(post_save)
def audit_log_save(sender, instance, created, **kwargs):
    if sender == AuditLog:
        return  # avoid recursion

    user = get_current_user()  

    action = 'CREATE' if created else 'UPDATE'
    old_data = None  # For updates, you can implement pre-save snapshot if desired
    new_data = model_to_dict(instance)

    audit_entry = AuditLog.objects.create(
        user=user,
        action=action,
        model_name=sender.__name__,
        object_id=str(instance.pk),
        old_data=old_data,
        new_data=new_data
    )

    # Publish after DB commit to avoid locking issues
    transaction.on_commit(lambda: publish_audit_log({
        'user': user.username if user else None,
        'action': action,
        'model_name': sender.__name__,
        'object_id': str(instance.pk),
        'timestamp': str(audit_entry.timestamp),
        'old_data': old_data,
        'new_data': new_data,
    }))


@receiver(pre_delete)
def audit_log_delete(sender, instance, **kwargs):
    if sender == AuditLog:
        return  # avoid recursion

    user = get_current_user()

    old_data = model_to_dict(instance)

    audit_entry = AuditLog.objects.create(
        user=user,
        action='DELETE',
        model_name=sender.__name__,
        object_id=str(instance.pk),
        old_data=old_data,
        new_data=None
    )

    transaction.on_commit(lambda: publish_audit_log({
        'user': user.username if user else None,
        'action': 'DELETE',
        'model_name': sender.__name__,
        'object_id': str(instance.pk),
        'timestamp': str(audit_entry.timestamp),
        'old_data': old_data,
        'new_data': None,
    }))
