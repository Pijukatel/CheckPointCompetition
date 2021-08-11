from django.contrib import messages


def message_decorator_factory(message_level, message_content):
    def message_decorator(func):
        """Decorator for adding custom messages to functions with requests."""

        def _add_message(request, *args, **kwargs):
            messages.add_message(request, message_level, message_content)
            return func(request, *args, **kwargs)

        return _add_message

    return message_decorator


staff_member_required_message = message_decorator_factory(
    messages.INFO, "Only staff members can confirm photos. Log in as staff member.")
