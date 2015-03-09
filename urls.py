from django.conf.urls import patterns, url
from simplechat import views

urlpatterns = patterns("",
    url(r"^$", views.Index.as_view(), name="index"),
    url(r"^api/room/", views.RoomList.as_view(), name="room_list"),
    url(r"^room/(?P<pk>\d+)", views.RoomView.as_view(), name="room_detail"),
)