"""venchmark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#generic imports
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.auth import views as auth_views
#generic views
from . import views


# this app
#from companies import views as CompanyViews
from assessments import views as AssessmentViews
from companies import views as CompanyViews
from rest_framework.authtoken import views as restviews
from wkhtmltopdf.views import PDFTemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.HomePageView.as_view(), name='home'),
    path('', views.logout_view, name='logout'),
    path('', views.redirect_home_view, name='login'),
    path('admin/', admin.site.urls),

    # Vendor URLS
    #path('companies/', include('companies.urls')),
    #path('people/', include('companies.urls')),

    #companies url patterns
    path('companies/', CompanyViews.CompanyListView.as_view(), name='company_list'),
    path('companies/new/', CompanyViews.CompanyCreateView.as_view(), name='company_new'),
    #path('company/update/<uuid:uuid>/', CompanyViews.CompanyUpdateView.as_view(), name='company_update'),
    path('company/update/<uuid:uuid>/', CompanyViews.CompanyUpdateView2.as_view(), name='company_update'),
    path('company/<uuid:uuid>/', CompanyViews.CompanyDetailView.as_view(), name='company_detail'),
    #path('company/<uuid:uuid>/delete', CompanyViews.CompanyDeleteView.as_view(), name='company_delete'),
    path('company/<uuid:uuid>/delete/', CompanyViews.CompanyDeleteView2.as_view(), name='company_delete'),

    #people url patterns
    path('people/', CompanyViews.UserListView.as_view(), name='user_list'),
    path('people/', include('django.contrib.auth.urls')), # new
    #path('people/new/', CompanyViews.UserCreateView.as_view(), name='NewUser'),
####    path('people/new/', CompanyViews.UserCreateView2.as_view(), name='user_new'),
    path('people/new/', CompanyViews.PersonCreateView.as_view(), name='user_new'),
    path('people/<uuid:uuid>/', CompanyViews.UserDetailView.as_view(), name='user_detail'),
    #path('people/update/<uuid:uuid>/', CompanyViews.UserUpdateView.as_view(), name='user_update'),
    path('people/update/<uuid:uuid>/', CompanyViews.PersonUpdateView.as_view(), name='user_update'),
    path('people/<uuid:uuid>/delete/', CompanyViews.UserDeleteView2.as_view(), name='user_delete'),
    #path('people/<uuid:uuid>/settings', CompanyViews.UserSettingsView.as_view(), name='user_settings'),
    #path('people/signup/', PeopleViews.SignUp.as_view(), name='signup'),
    #path('people/settings/', PeopleViews.Settings.as_view(), name='settings'),
    #path('get-user-auth-token/', restviews.obtain_auth_token, name='get_user_auth_token'),
    #path('people/login/', auth_views.login, name='login'),
    #path('people/logout/', auth_views.logout, name='logout'),
    #path('vendors/new/', CompanyViews.VendorCreateView.as_view(), name='NewVendor'),
    #path('vendor/update/<int:pk>/', CompanyViews.VendorUpdateView.as_view(), name='vendor_update'),
    #path('vendor/<int:pk>/', CompanyViews.VendorDetailView.as_view(), name='vendor_detail'),
    #path('vendor/<int:pk>/delete', CompanyViews.VendorDeleteView.as_view(), name='vendor_delete'),

    # framework source URLs
    #path('sources/', AssessmentViews.FrameworkSourceListView.as_view(), name='frameworksource_list'),
    #path('source/update/<int:pk>/', AssessmentViews.FrameworkSourceUpdateView.as_view(), name='frameworksource_update'),
    #path('source/<slug:id>/', AssessmentViews.FrameworkSourceDetailView.as_view(), name='frameworksource_detail'),
    #path('source/<int:pk>/delete', AssessmentViews.FrameworkSourceDeleteView.as_view(), name='frameworksource_delete'),
    path('source/new/', AssessmentViews.FrameworkSourceCreateView.as_view(), name='frameworksource_new'),

    # framework URLS
    # frameworks plural
    path('frameworks/', AssessmentViews.FrameworkListView.as_view(), name='framework_list'),
    path('frameworks/new/', AssessmentViews.FrameworkCreateView.as_view(), name='NewFramework'),

    # framework singular
    path('framework/update/<uuid:uuid>/', AssessmentViews.FrameworkUpdateView2.as_view(), name='framework_update'),
    path('framework/<uuid:uuid>/', AssessmentViews.FrameworkDetailView.as_view(), name='framework_detail'),
    path('framework/<uuid:uuid>/delete/', AssessmentViews.FrameworkDeleteView2.as_view(), name='framework_delete'),
    path('framework/clone/<uuid:uuid>/',  AssessmentViews.CloneFramework.as_view(), name='framework_clone'),
    # path('framework/clone/<uuid:uuid>/',  AssessmentViews.RequestToCloneFramework, name='framework_clone'),

    # framework controls URLS
    path('controls/<uuid:uuid>/',  AssessmentViews.FrameworkControlsListView.as_view(), name='controls_list'),
    path('controls/<uuid:uuid>/add-single/',  AssessmentViews.FrameworkControlsAddView.as_view(), name='control_add'),
    #path('controls/<uuid:uuid>/add-multiple/',  AssessmentViews.FrameworkControlsAddMultipleView.as_view(), name='controls_add'),
    path('controls/<uuid:uuid>/add-multiple/',  AssessmentViews.upload_multiple_controls_file, name='controls_add'),

    #path('controls/<uuid:uuid>/upload/',  AssessmentViews.FrameworkControlsUploadView, name='controls_update'),
    #path('control/update/<slug:id>/', AssessmentViews.FrameworkControlsUpdateView.as_view(), name='control_update'),
#    path('control/<slug:id>/', AssessmentViews.FrameworkControlsDetailView.as_view(), name='control_detail'),
#    path('control/<slug:id>/views.delete', AssessmentViews.FrameworkControlsDeleteView.as_view(), name='control_delete'),
    path('control/new/', AssessmentViews.FrameworkControlsCreateView.as_view(), name='control_new'),
    path('control/addToFramework/<uuid:uuid>/', AssessmentViews.FrameworkControlsAddView.as_view(), name='control_new'),
    path('control/<uuid:uuid>/', AssessmentViews.FrameworkControlsDetailView.as_view(), name='control_detail'),
    path('control/<uuid:uuid>/delete/', AssessmentViews.FrameworkControlsDeleteView.as_view(), name='control_delete'),
    path('control/update/<uuid:uuid>/', AssessmentViews.FrameworkControlsUpdateView.as_view(), name='control_update'),

    # assessments URLS
    path('assessments/',  AssessmentViews.AssessmentListView.as_view(), name='assessment_list'),
    path('assessments/new/', AssessmentViews.AssessmentCreateView.as_view(), name='NewAssessment'),
    #path('assessments/new/', AssessmentViews.assessment_entry, name='NewAssessment'),
    path('assessment/update/<uuid:uuid>/', AssessmentViews.AssessmentUpdateView2.as_view(), name='assessment_update'),
    #path('assessment/<uuid:uuid>/', AssessmentViews.AssessmentUpdateView.as_view(), name='assessment_detail'),
    path('assessment/<uuid:uuid>/delete/', AssessmentViews.AssessmentDeleteView2.as_view(), name='assessment_delete'),
    path('assessment/<uuid:uuid>/questions/',  AssessmentViews.QuestionsCreateView.as_view(), name='NewQuestions'),
    path('assessment/<uuid:uuid>/status/',  AssessmentViews.AssessmentStatusView.as_view(), name='assessment_status'),
    #path('assessment/<uuid:uuid>/status-change/',  AssessmentViews.AssessmentStatusChangeView.as_view(), name='assessment_status_change'),


    path('assessment/<uuid:uuid>/status-change/',  AssessmentViews.AssessmentStatusChange, name='assessment_status_change'),

    # analysis URLS
    path('analysis/', AssessmentViews.AnalysisListView2.as_view(), name='analysis_list'),
    path('analysis/<uuid:uuid>/', AssessmentViews.AnalysisQuestionListView.as_view(), name='analysis_q_list'),
    path('analysis/update/<uuid:uuid>/', AssessmentViews.AnalysisUpdateView.as_view(), name='analysis_new'),

    # questionnaire URLS
    #path('questionnaire/<uuid:uuid>/analyst/', AssessmentViews.AnalystContactQuestionnaireView.as_view(), name='analyst_questionnaire_detail'),
    #path('questionnaire/<uuid:uuid>/vendor/', AssessmentViews.VendorQuestionnaireView.as_view(), name='vendor_questionnaire_detail'),
    path('questionnaires/',  AssessmentViews.QuestionnaireListView.as_view(), name='questionnaire_list'),
    path('questionnaire/<uuid:uuid>/', AssessmentViews.VendorQuestionListView2.as_view(), name='questions_list'),
    path('questionnaire/<uuid:uuid>/approved/', AssessmentViews.VendorQuestionListApproved, name='questions_approved'),
    #path('questionnaire/<uuid:quuid>/', AssessmentViews.VendorQuestionListView.as_view(), name='questions_list_success'),
    path('question/update/<uuid:uuid>/', AssessmentViews.QuestionUpdateView.as_view(), name='answer_new'),
    path('question/<uuid:uuid>/update/', AssessmentViews.QuestionUpdateView2, name='answer_new'),
    path('answer/<uuid:uuid>/update/', AssessmentViews.answer_update, name="update_answer"),
    path('answer/<uuid:uuid>/evidence/', AssessmentViews.UploadDocument, name="answer_evidence"),
    path('answer/evidence/add/', AssessmentViews.DocumentCreateView.as_view(), name='create_document'),

    # assessments URLS
    path('reports/',  AssessmentViews.ReportListView.as_view(), name='report_list'),
    path('report/<uuid:uuid>/',  AssessmentViews.ReportDetailView.as_view(), name='report_detail'),
    path('report/<uuid:uuid>/edit/',  AssessmentViews.ReportEditView.as_view(), name='report_edit'),
    #path('report/generate/<uuid:uuid>/',  AssessmentViews.ReportGenerateView.as_view(), name='report_generate'),
    path('report/<uuid:uuid>/update/', AssessmentViews.report_update, name="update_report"),
    path('report/generate/<uuid:uuid>/',  AssessmentViews.GenerateReport, name='report_generate'),
    #url(r'^pdf/$', PDFTemplateView.as_view(template_name='my_template.html', filename='my_pdf.pdf'), name='pdf'),
    #path('report/pdf/<uuid:uuid>/', AssessmentViews.ReportDetailPdf2.as_view(), name='report-pdf'),
    path('report/<uuid:uuid>/pdf/', AssessmentViews.ReportDetailPDFView.as_view(), name='report-pdf'),
    path('report/<uuid:uuid>/docx/', AssessmentViews.ReportDetailDOCXView3, name='report-docx'),

    #path('report/pdf/<uuid:uuid>/', AssessmentViews.ReportPDF.as_view(), name='report-pdf'),
    #path('report/pdf/<uuid:uuid>/', AssessmentViews.ReportDetailPdf.as_view()),

    #path('report/pdf/<uuid:uuid>/', AssessmentViews.MyPdfView.as_view(), name='report-pdf'),

    #path('report/pdf/<uuid:uuid>/', PDFTemplateView.as_view(template_name='assessments/templates/assessments/report_pdf_detail.html', filename='report.pdf'), name='pdf'),

    # api urls
    path('api/v1/', include('api.urls')),


    ## 2020-0619 - DB - for CompanyAutocomplete
    path('company-autocomplete/', CompanyViews.CompanyAutocomplete.as_view(), name='company-autocomplete'),
    path('user-autocomplete/', CompanyViews.UserAutocomplete.as_view(), name='user-autocomplete'),
    #path('states-autocomplete/', CompanyViews.StatesAutocomplete.as_view(), name='states-autocomplete'),

    #redirect_home_view
    path('redirect-home/', views.redirect_home_view, name='redirect'),
    #path('change-password/', auth_views.PasswordChangeView.as_view(template_name='commons/change-password.html', success_url = '/'), name='change_password'),
    path(
            'change-password/',
            auth_views.PasswordChangeView.as_view(
                template_name='change-password.html',
                success_url = '/'
            ),
            name='change_password'
        ),


    path('password-reset/',
     auth_views.PasswordResetView.as_view(
         #template_name='commons/password-reset/password_reset.html',
         template_name='password_reset.html',
         subject_template_name='password_reset_subject.txt',
         html_email_template_name='password_reset_email.html',
         # success_url='/login/'
     ),
     name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ),
         name='password_reset_complete'),
    #path('password-reset/', views.PasswordChangePageView, name='password-change'),

    #path('users/', include('users.urls')),
    #path('users/', include('django.contrib.auth.urls')),

    # search urls
    path('search/', include('search.urls')),
    #path('redirect-home/', views.redirect_home_view, name='redirect')
    #path('', include('pages.urls')),
    #path('users/', include('django.contrib.auth.urls')),
    #path('configs/', include('configs.urls')),
    #path('analysis/', include('analysis.urls')),
    #path('reports/', include('reports.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
