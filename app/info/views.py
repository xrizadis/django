from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag, Component
from info import serializers


class TagViewSet(viewsets.GenericViewSet,
                 mixins.CreateModelMixin,
                 mixins.ListModelMixin):
    """manage tags in database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """return only for current user"""
        print(self.request.user)
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """create new tag"""
        serializer.save(user=self.request.user)


class ComponentViewSet(viewsets.GenericViewSet,
                       mixins.CreateModelMixin,
                       mixins.ListModelMixin):
    """manage components in database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Component.objects.all()
    serializer_class = serializers.ComponentSerializer

    def get_queryset(self):
        """return only for current user"""
        print(self.request.user)
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """create new tag"""
        serializer.save(user=self.request.user)
