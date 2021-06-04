from django.shortcuts import render,redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User


class BitsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if '/logout' not in request.path and '/admin' not in request.path:

            current_user = request.user

            if current_user.is_authenticated:
                if current_user.is_superuser:
                    response = self.get_response(request)
                    return response
                else:
                    extradata = SocialAccount.objects.filter(user=current_user).first().extra_data
                    # if request.get_full_path() is not "https://bits-assist-2.herokuapp.com/logout/":
                    if "hd" not in extradata:
                        messages.warning(request, f'Login with BITS ID')
                        User.objects.filter(id=current_user.id).delete()
                        return redirect("/logout")

            # Code to be executed for each request before
            # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response