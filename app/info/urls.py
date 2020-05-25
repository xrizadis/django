from django.urls import path, include
from rest_framework.routers import DefaultRouter
from info import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
app_name = "info"


urlpatterns = [
    path('', include(router.urls))
]
