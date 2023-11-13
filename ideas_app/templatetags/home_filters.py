from django import template

register = template.Library()

@register.filter
def should_show_interested(notification_sent, idea):
    for notification in notification_sent:
        if notification.notification_to_id == idea.fk_user_profile_id.fk_user_id.id and idea.post_heading in notification.notification_message:
            return False
    return True
