# api/urls.py
from django.urls import include, path

from . import views

urlpatterns = [
    path('assessments/', views.ListAssessments.as_view()),
    path('assessments/ongoing/', views.AssessmentsOngoing5ListAPIVIew.as_view()),
    #path('assessments/<int:pk>', views.DetailAssessments.as_view()),

    #path('assessments/questions/', views.ListQuestions.as_view()),
    path('assessment/<uuid:uuid>/', views.AssessmentDetailsAPIVIew.as_view()),
    path('assessment/<uuid:uuid>/compliance/', views.RetrieveSingleCompanyComplianceAPIView.as_view()),
    path('assessment/<uuid:uuid>/risk/', views.RetrieveSingleCompanyRiskAPIView.as_view()),
    #path('assessment/questions/<int:pk>/', views.DetailQuestions.as_view()),
    #path('frameworks/', views.ListFrameworks.as_view()),
    path('frameworks/', views.RetrieveAllFrameworksAPIView.as_view()),
    path('frameworks/<slug:id>/', views.DetailFrameworks.as_view()),
    path('framework/controls/<slug:id>/', views.RetrieveControlsByFramework.as_view()),
    path('controls/<uuid:uuid>/', views.RetrieveControls.as_view()),
    path('control/<uuid:uuid>/', views.RetrieveSingleControl.as_view()),
    path('companies/', views.RetrieveAllCompaniesAPIView.as_view()),
    path('companies/<uuid:uuid>/', views.RetrieveCompaniesAPIView.as_view()),
    path('companies/data/', views.RetrieveCompaniesDataAPIView.as_view()),
    path('companies/risk/', views.RetrieveCompaniesRiskAPIView.as_view()),
    path('people/', views.RetrieveAllUsersAPIView.as_view()),
    path('people/<uuid:uuid>/', views.RetrieveUserAPIView.as_view()),
    path('questions/<uuid:uuid>/', views.RetrieveQuestionsbyAssessmentAPIView.as_view()),
    path('reports/', views.ReportsListAPIVIew.as_view()),

    #path('search/', views.SearchAPIView.as_view()),
    # path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/', include('dj_rest_auth.urls')),  # was dj-rest-auth/
]
