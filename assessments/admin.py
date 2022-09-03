from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import Assessment, Questionnaire, Question, Framework, FrameworkSource, FrameworkControls
from .forms import AssessmentFrameworkChangeListForm
# Register your models here.

# Framework Administration\
class FrameworkAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'short_name', 'version', 'publication_date', 'source')
admin.site.register(Framework, FrameworkAdmin)

# Framework Source Administration
class FrameworkSourceAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'acronym', 'url')
admin.site.register(FrameworkSource, FrameworkSourceAdmin)

#Framework Controls Administration
class FrameworkControlsAdmin(admin.ModelAdmin):
    list_display = ('framework', 'function', 'category', 'subcategoryID', 'subcategory', 'reference', 'default_question')
admin.site.register(FrameworkControls, FrameworkControlsAdmin)

class AssessmentFrameworkChangeList(ChangeList):
    def __init__(self, request, model, list_display,
        list_display_links, list_filter, date_hierarchy,
        search_fields, list_select_related, list_per_page,
        list_max_show_all, list_editable, model_admin, sortable_by):

        super(AssessmentFrameworkChangeList, self).__init__(request, model,
            list_display, list_display_links, list_filter,
            date_hierarchy, search_fields, list_select_related,
            list_per_page, list_max_show_all, list_editable,
            model_admin, sortable_by)

        # these need to be defined here, and not in MovieAdmin
        self.list_display = ['action_checkbox', 'name', 'frameworks']
        self.list_display_links = ['name']
        self.list_editable = ['frameworks']


# Assessment Administration
class AssessmentAdmin(admin.ModelAdmin):
    #list_display = ( 'name', 'vendor', 'owner', 'vendor_contact', 'auditor', 'analyst', 'status' )
    def get_changelist(self, request, **kwargs):
        return AssessmentFrameworkChangeList

    def get_changelist_form(self, request, **kwargs):
        return AssessmentFrameworkChangeListForm

admin.site.register(Assessment, AssessmentAdmin)

# Assessment Questionnaire Administration
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'assessment')
admin.site.register(Questionnaire, QuestionnaireAdmin)

# Assessment Questions Administration
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'assessment', 'questionnaire', 'question', 'answer', 'notes', 'likelihood', 'impact', 'risk_rating')
admin.site.register(Question, QuestionAdmin)
