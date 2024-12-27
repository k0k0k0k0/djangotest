from django.urls import path

from . import views
#from .views import indexview

urlpatterns = [
    path("", views.indexview, name="index"),
    path("top/<int:num>/extensions/", views.extstats, name="extstats"),
    path("top/<int:num>/bysize/", views.sizetop, name="sizetop"),
    path("top/<int:num>/bydimensions/", views.imgtop, name="imgtop"),
    path("top/<int:num>/bypages/", views.pagetop, name="pagetop"),
]