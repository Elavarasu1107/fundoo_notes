from .models import UserLog


class UserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.user_log(request)
        return response

    def user_log(self, request):
        user_data = UserLog.objects.filter(method=request.method, url=request.get_full_path())
        if not user_data.exists():
            UserLog.objects.create(method=request.method, url=request.get_full_path())
        else:
            user = user_data.first()
            user.count += 1
            user.save()
