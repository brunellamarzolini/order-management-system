# oms/mixins.py
from django.core.cache import cache
from rest_framework.response import Response
from localization.helpers import get_language_from_request

class CacheListResponseMixin:

    def get_cache_list_key(self, request):
        lang = get_language_from_request(request)
        query = request.GET.urlencode()
        params = f":{query}" if query else ""
        return f"{self.basename}:list:{lang.code}{params}"

    def list(self, request, *args, **kwargs):
        cache_key = self.get_cache_list_key(request)
        data = cache.get(cache_key)
        if data is not None:
            return Response(data)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data)
        return response
    
class CacheDetailResponseMixin:

    def get_cache_detail_key(self, request, obj=None, pk=None):
        page_pk = pk or (self.kwargs.get('pk') if hasattr(self, 'kwargs') else None)
        lang = get_language_from_request(request)
        return f"{self.basename}:detail:{page_pk}:{lang.code}"

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cache_key = self.get_cache_detail_key(request, pk=pk)
        data = cache.get(cache_key)
        if data is not None:
            return Response(data)
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data)
        return response