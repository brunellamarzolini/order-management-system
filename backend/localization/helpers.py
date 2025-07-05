from django.utils.translation import get_language_from_request as dj_get_language_from_request
from django.conf import settings
from localization.models import Language

def get_language_from_request(request, check_path=True):

    # todo spostarlo in un middleware
    if hasattr(request, "lang_info"):
        return request.lang_info
    
    lang = dj_get_language_from_request(request, check_path=check_path)
    lang = lang.lower().split("-")[0]
    try:
        lang_model = Language.objects.get(code=lang)
    except Language.DoesNotExist:
        lang_model = Language.objects.get(code=settings.DEFAULT_LANG)

    request.lang_info = lang_model
    return lang_model