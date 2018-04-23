from django.conf.urls import url

from . import views

urlpatterns = [
    url( r'^index', views.index, name='index' ),
    url( r'^survey', views.survey, name='survey' ),
    url( r'^results/$', views.results, name='results' ),
    url( r'^sort_results/$', views.sort_results, name='sort_results' ),
    url( r'^submit_survey', views.submit_survey, name='submit_survey' )
]