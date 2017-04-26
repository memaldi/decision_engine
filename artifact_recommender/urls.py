from django.conf.urls import url
from artifact_recommender import views

urlpatterns = [
    url(r'^dataset/$', views.DatasetList.as_view()),
    url(r'^dataset/(?P<pk>[0-9]+)/$', views.DatasetDetail.as_view()),
    url(r'^dataset/(?P<pk>[0-9]+)/recommend/datasets/$',
        views.DatasetRecommendDataset.as_view()),
    url(r'^buildingblock/$', views.BuildingBlockList.as_view()),
    url(r'^buildingblock/(?P<pk>[0-9]+)/$',
        views.BuildingBlockDetail.as_view()),
    url(r'^app/$', views.ApplicationList.as_view()),
    url(r'^app/(?P<pk>[0-9]+)/$', views.ApplicationDetail.as_view()),
    url(r'^idea/$', views.IdeaList.as_view()),
    url(r'^idea/(?P<pk>[0-9]+)/$', views.IdeaDetail.as_view()),
]
