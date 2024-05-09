from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response


class CreateViewSetMixin(viewsets.ModelViewSet):
    model = None

    def get_model(self):
        if self.model is None:
            raise ImproperlyConfigured('You must provide a model')
        return self.model

    def get_serializer_class(self):
        if self.serializer_post_class is None:
            raise ImproperlyConfigured('You must specify a serializer class!!!!!!')
        if self.action in ['list', 'retrieve']:
            return self.serializer_class
        return self.serializer_post_class

    def create(self, request, *args, **kwargs):
        obj_id = super().create(request, *args, **kwargs).data.get('id')
        obj = get_object_or_404(self.get_model(), id=obj_id)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status.HTTP_201_CREATED)

