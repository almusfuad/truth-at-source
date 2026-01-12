from app.models import AuditLog


def write_audit(actor, action, obj, metadata=None):
    log = AuditLog(
        actor_user_id=actor.user_id,
        actor_role=actor.role,
        action=action,
        object_type=obj.__class__.__name__,
        object_id=str(obj.id),
    )
    log.set_metadata(metadata or {})
    log.save()
