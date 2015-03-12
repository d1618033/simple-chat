from django.conf.urls import patterns, url
from simplechat_api import views


urlpatterns = patterns("",
    url(r"^room/$", views.RoomList.as_view(), name="room_list"),
    url(r"^room/(?P<pk>\d+)$", views.RoomDetail.as_view(), name="room_detail"),
    url(r"^participant/$", views.ParticipantList.as_view(), name="participant_list"),
    url(r"^participant/(?P<pk>\d+)/$", views.ParticipantDetail.as_view(), name="participant_detail"),
)