from django.contrib.sites.models import Site
from django.urls import reverse


def activation_url(url_name, token):
    site = Site.objects.get_current()
    domain = site.domain
    relative_url = f"{reverse(url_name)}?token={token}"
    activation_url = f'{domain}{relative_url}'
    return activation_url
