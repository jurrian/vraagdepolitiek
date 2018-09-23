from django.contrib.sites.middleware import CurrentSiteMiddleware as DjangoCurrentSiteMiddleware
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist


class CurrentSiteMiddleware(DjangoCurrentSiteMiddleware):
    """
    Middleware that sets `site` attribute to request object.
    If the site does not exists it returns None instead.
    """

    def process_request(self, request):
        try:
            request.site = get_current_site(request)
        except ObjectDoesNotExist:
            request.site = None
