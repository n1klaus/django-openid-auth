import json
import logging

from django.shortcuts import redirect
from django.shortcuts import render
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

logger = logging.getLogger("mozilla_django_oidc")


def openid_index(request):
    logger.debug("Displaying user:", request.session.__dict__)
    return render(
        request,
        "openid.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )


class MyOpenIdConnectBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        logger.debug("Creating user:", claims)
        user = super().create_user(claims)
        # Customize user creation here
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()
        return user

    def update_user(self, user, claims):
        logger.debug("Updating user:", claims)
        # user = super().update_user(user, claims)
        # Customize user update here
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()
        return user
