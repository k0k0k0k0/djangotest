from django.urls import path

from . import views
#from .views import indexview

urlpatterns = [
    # ex: /polls/
    path("", views.indexview, name="index"),
    # ex: /polls/5/
    path("top/<int:num>/extensions/", views.extstats, name="extstats"),
    # ex: /polls/5/results/
    path("top/<int:num>/bysize/", views.sizetop, name="sizetop"),
    # ex: /polls/5/vote/
    path("top/<int:num>/bydimensions/", views.imgtop, name="imgtop"),
    path("top/<int:num>/bypages/", views.pagetop, name="pagetop"),
]