from django.conf.urls import patterns, url
from simplechat_api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'room', views.RoomViewSet)
router.register(r'participant', views.ParticipantViewSet)
urlpatterns = router.urls

