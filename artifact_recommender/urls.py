from django.conf.urls import url
from artifact_recommender import views

urlpatterns = [
    url(r'^dataset/$', views.DatasetList.as_view()),
    url(r'^dataset/(?P<pk>[0-9]+)/$', views.DatasetDetail.as_view()),
    url(r'^tag/$', views.TagList.as_view()),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagList.as_view()),
]
