import json
import logging

from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

logger = logging.getLogger(__name__)


def openid_index(request):
    return render(request, "openid.html")


class MyOpenIdConnectBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super().create_user(claims)
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()
        return user

    def update_user(self, user, claims):
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()
        return user

    def get_redirect_url(self, request, next_url, **kwargs):
        # Validate the next_url before redirecting
        if next_url and "://" not in next_url:
            return reverse(next_url)
        return super().get_redirect_url(request, next_url, **kwargs)
