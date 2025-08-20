from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def can_view_button(context, action, model_name):
    """
    action: add, change, delete, view
    model_name: nom du modèle (ex: departement, quartier, etc.)
    """
    user = context['user']

    if not user.is_authenticated:
        return False

    group_permissions = {
        'SUPERADMIN': ['add', 'change', 'delete', 'view'],
        'ADMIN': ['add', 'change', 'view'],
        'UTILISATEUR': ['view'],
    }

    for group_name, permissions in group_permissions.items():
        if getattr(user, f'is_{group_name.lower()}', False):
            return action in permissions

    return False
