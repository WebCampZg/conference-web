from django.core.exceptions import PermissionDenied

from functools import wraps


def require_ticket_holder(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.user.is_ticket_holder():
            return f(request, *args, **kwargs)
        else:
            raise PermissionDenied("You have to be a ticket holder to access this page.")
    return wrapper

