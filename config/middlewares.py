from django.utils.translation import activate
from django.conf import settings


class ActivateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if language:
            language = language.strip(',')[0]
            activate(language)
        else:
            activate(settings.LANGUAGE_CODE)

        response = self.get_response(request)
        return response
