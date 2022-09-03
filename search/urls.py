from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#from django.views.generic import list_detail  ### something imported to test two-model view
from . import views


urlpatterns = [
    path('', views.SearchResultsView.as_view(), name='search_results'),
    ]
