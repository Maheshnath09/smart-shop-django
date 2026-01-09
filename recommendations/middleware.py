"""
Middleware to ensure session exists for guest user tracking
"""


class EnsureSessionMiddleware:
    """
    Ensures that a session key exists for all users,
    even if they haven't logged in. This is needed for
    tracking product views for guest users.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Create session if it doesn't exist
        if not request.session.session_key:
            request.session.create()
        
        response = self.get_response(request)
        return response
