from django.conf.urls import url
from artifact_recommender import views

urlpatterns = [
    url(r'^dataset/$', views.DatasetList.as_view()),
    url(r'^dataset/(?P<pk>[0-9]+)/$', views.DatasetDetail.as_view()),
    url(r'^buildingblock/$', views.BuildingBlockList.as_view()),
    url(r'^buildingblock/(?P<pk>[0-9]+)/$',
        views.BuildingBlockDetail.as_view()),
    url(r'^app/$', views.ApplicationList.as_view()),
    url(r'^app/(?P<pk>[0-9]+)/$', views.ApplicationDetail.as_view()),
]
