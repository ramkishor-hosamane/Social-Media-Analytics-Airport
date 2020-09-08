
from . import views

from django.urls import path,include
from django.conf.urls import url
urlpatterns = [
        path('home',views.index,name="home"),
        url(r'^do_analysis/$', views.bg_work, name='do_analysis'),
        path('scrapping',views.scrapping,name="scrapping"),
        url(r'^analysis/$', views.analysis, name='analysis'),
        path('about',views.about,name="about"),
        path('',views.index,name="home"),

]
