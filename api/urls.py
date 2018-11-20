from django.conf.urls import url
from api import views

urlpatterns = [
    # url(r'^asset/$',views.asset),
    url(r'^asset/$',views.AssetView.as_view()),
    url(r'^test/$', views.TestView.as_view()),
    url(r'^orm/$', views.OrmView.as_view()),
    # url(r'^detail/$', views.detail)
]
