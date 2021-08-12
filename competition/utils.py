from django.contrib import messages


def user_is_not_staff(request):
    return not(request.user.is_active and request.user.is_staff)


def message_decorator_factory(message_level, message_content, condition_function):
    def message_decorator(func):
        """Decorator for adding custom messages to functions with requests."""

        def _add_message(request, *args, **kwargs):
            if condition_function(request):
                messages.add_message(request, message_level, message_content)
            return func(request, *args, **kwargs)

        return _add_message

    return message_decorator


staff_member_required_message = message_decorator_factory(
    messages.INFO,
    "Only staff members can confirm photos. Log in as staff member.",
    user_is_not_staff)
