from django.shortcuts import redirect

class SuperuserRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Check if the user is trying to access the admin login and is a superuser
        if request.path == '/admin/login/' and request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('inventory/admin_dashboard')  # Redirect to a named URL
        return response