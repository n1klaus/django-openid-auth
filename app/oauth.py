import json
from urllib.parse import quote_plus
from urllib.parse import urlencode

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("oauth_index")))


def logout(request):
    request.session.clear()
    return redirect(
        "https://{}/v2/logout?{}".format(
            settings.AUTH0_DOMAIN,
            urlencode(
                {
                    "returnTo": request.build_absolute_uri(reverse("oauth_index")),
                    "client_id": settings.AUTH0_CLIENT_ID,
                },
                quote_via=quote_plus,
            ),
        )
    )


def oauth_index(request):
    return render(
        request,
        "oauth.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )
