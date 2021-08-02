class SelfForUser:
    """Returns user object for logged user."""

    def get_object(self):
        return self.request.user