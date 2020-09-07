
from . import views

from django.urls import path,include

urlpatterns = [
        path('home/',views.index,name="home"),
        path('scrapping',views.scrapping,name="scrapping"),
        path('analysis',views.analysis,name="analysis"),
        path('about',views.about,name="about"),
        path('',views.index,name="home"),

]
