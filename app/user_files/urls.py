from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user_files import views

#/api/user_files/tags/1/
#default router automatically register approperiate actions for the viewsets

router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'user_files'

urlpatterns = [
    path('', include(router.urls))
]
