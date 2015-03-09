from django.conf.urls import patterns, url
from simplechat import views

urlpatterns = patterns("",
    url("^$", views.Index.as_view(), name="index"),
)