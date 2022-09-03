#assessments/forms.py
import datetime

from dal import autocomplete
from django import forms
from tempus_dominus.widgets import DatePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Field
from . models import Assessment, Framework, FrameworkSource, FrameworkControls, Questionnaire, Question, AssessmentFrameworks, Report, Document
from companies.models import Company, User
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from django.forms.widgets import CheckboxSelectMultiple
from bootstrap_modal_forms.forms import BSModalForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from . widgets import BootstrapSelect





class NewAssessmentForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'size': '75','placeholder': 'Assessment Name ...'}))
    #status = forms.ChoiceField(choices=STATUS)
    #vendor = forms.ModelChoiceField(queryset=Company.objects.all())
    vendor = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=autocomplete.ModelSelect2(url='company-autocomplete'),
        label="Company"
    )
    vendor_contact = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user-autocomplete'),
        label="Vendor Point of Contact:",
    )
    analyst = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user-autocomplete'),
        label="Analyst:",
    )
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user-autocomplete'),
        label="Relationship Owner:",
    )
    #vendor_contact = forms.ModelChoiceField(User.objects.all(), widget=BootstrapSelect())
    #vendor_contact = forms.ModelChoiceField(queryset=User.objects.all())
    #vendor_contact = forms.ModelChoiceField(
    #    queryset=User.objects.all(),
    #    widget=autocomplete.ModelSelect2(url='user-autocomplete'),
    #    label="Vendor Point of Contact"
    #)
    #owner = forms.ModelChoiceField(User.objects.all(), widget=BootstrapSelect())
    #analyst = forms.ModelChoiceField(User.objects.all(), widget=BootstrapSelect())

    #auditor = forms.ModelChoiceField(User.objects.all(), required=False)
    #analyst = forms.ModelChoiceField(User.objects.all(), required=False)
    #start_date = forms.DateTimeField(
    #    input_formats=['%d/%m/%Y %H:%M'],
    #    widget=BootstrapDateTimePickerInput()
    #    )


    class Meta:
        model = Assessment
        #exclude = ['id']
        fields = [ 'name', 'vendor', 'owner', 'vendor_contact', 'start_date', 'auditor', 'analyst', 'frameworks' ]
        widgets = {
            'start_date': DatePicker(
                options={
                    'format': 'MM/DD/YYYY'
                },
                attrs={
                    'append': 'fa fa-calendar',
                },
            )
        }



    def CreateQuestionnaire(self, uuid):
        NewQuestionnaire = Questionnaire()
        NewQuestionnaire.assessment = Assessment.objects.filter(uuid=uuid).first()
        NewQuestionnaire.save()

    def PopulateQuestions(self, uuid):
        questionnaire = Questionnaire.objects.filter(assessment=uuid).first()
        aframework_set = AssessmentFrameworks.objects.filter(assessment=uuid)

        for afwork in aframework_set:
            #print("Processing framework:" + str(afwork.framework.name))
            controls_set = FrameworkControls.objects.filter(framework=afwork.framework)
            for ctrl in controls_set:
                print("Processing control: " + ctrl.categoryID)
                NewQuestion = Question()
                NewQuestion.questionnaire = questionnaire
                NewQuestion.assessment = questionnaire.assessment
                NewQuestion.control = ctrl
                NewQuestion.question = ctrl.default_question
                NewQuestion.save()


    def __init__(self, *args, **kwargs):
        super(NewAssessmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-8 mb-0'),
                Column('vendor', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                #Column('status', css_class='form-group col-md-4 mb-0'),
                Column('vendor_contact', css_class='form-group col-md-4 mb-0'),
                Column('owner', css_class='form-group col-md-4 mb-0'),
                Column('analyst', css_class='form-group col-md-4 mb-0'),

            ),
            Row(
                Column('start_date', css_class='form-group col-md-4 mb-0'),
                Column('frameworks', css_class='form-group col-md-6 mb-0')
            ),
            #Submit('submit', 'Create Assessment')
        )
        self.helper.add_input(Submit('submit', 'Create Assessment'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )
        self.fields["frameworks"].widget = CheckboxSelectMultiple()
        self.fields["frameworks"].queryset = Framework.objects.all()

class AssessmentListForm(forms.Form):
    class Meta:
        model = Assessment
        fields = [ 'name', 'vendor', 'owner', 'status', 'frameworks' ]

class AssessmentDetailForm(forms.Form):
    class Meta:
        model = Assessment
        fields = [ 'name', 'vendor', 'owner', 'vendor_contact', 'auditor', 'analyst', 'status', 'frameworks' ]
        #fields = ['CompanyName', 'CompanyURL']

#class AssessmentModifyForm(forms.Form):
class AssessmentModifyForm(forms.Form):
    #Vendor = forms.ModelChoiceField(queryset=Vendor.objects.all())
    class Meta:
        model = Assessment
        #fields = '__all__'
        fields = [ 'name', 'vendor', 'owner', 'vendor_contact', 'auditor', 'analyst', 'status', 'frameworks' ]

class AssessmentDeleteForm(forms.ModelForm):
    helper = FormHelper()
    helper.layout = Layout(
            Submit('submit', 'Save', css_class="btn btn-outline-success"),
            HTML("""&lt;a href="{% url "assessment_list" %}" class="btn btn-secondary"&gt;Cancel&lt;/a&gt;"""),
            HTML("""{% if object %}
                    &lt;a href="{% url "assessment-delete" object.id %}"
                    class="btn btn-outline-danger pull-right"&gt;
                    Delete &lt;i class="fa fa-trash-o" aria-hidden="true"&gt;&lt;/i&gt;&lt;/button&gt;&lt;/a&gt;
                    {% endif %}"""),
    )

### 2020-04-03 - DB - Migrating Frameworks forms to Assessments forms

#class FrameworkForm(ModelForm):
class FrameworkForm(BSModalForm):
    class Meta:
        model = Framework
        #exclude = ['id']
        fields = ['name', 'short_name', 'version', 'publication_date', 'source']

#class FrameworkAddForm(ModelForm):
class FrameworkAddForm(BSModalForm):
    class Meta:
        model = Framework
        #exclude = ['id']
        fields = ['name', 'short_name', 'version', 'publication_date', 'source']

#class FrameworkListForm(forms.Form):
class FrameworkListForm(BSModalForm):
    class Meta:
        model = Framework
        fields = ['name', 'short_name', 'version', 'publication_date', 'source']

class FrameworkDetailForm(forms.Form):
    class Meta:
        model = Framework
        fields = ['name', 'short_name', 'version', 'publication_date', 'source']
        #fields = ['CompanyName', 'CompanyURL']

class FrameworkModifyForm(forms.Form):
    class Meta:
        model = Framework

class FrameworkSourceAddForm(forms.ModelForm):
    class Meta:
        model = FrameworkSource
        #exclude = ['id']
        fields = ['name', 'acronym', 'url']

class FrameworSourcekListForm(forms.Form):

    class Meta:
        model = FrameworkSource
        fields = ['name', 'acronym', 'url']

class FrameworkSourceDetailForm(forms.Form):
    class Meta:
        model = FrameworkSource
        fields = ['name', 'acronym', 'url']
        #fields = ['CompanyName', 'CompanyURL']

class FrameworkSourceModifyForm(forms.Form):
    class Meta:
        model = FrameworkSource
        fields = ['name', 'acronym', 'url']

class FrameworkControlsAddForm(forms.ModelForm):
    class Meta:
        model = FrameworkControls
        #exclude = ['id']
        fields = ['framework', 'function', 'category', 'subcategoryID', 'subcategory', 'reference', 'default_question']

#class FrameworkControlsListForm(forms.Form):

#    class Meta:
#        model = FrameworkControls
#        fields = ['Name', 'Acronym', 'URL']

class FrameworkControlsDetailForm(forms.Form):
    class Meta:
        model = FrameworkControls
        fields = ['framework', 'function', 'category', 'subcategoryID', 'subcategory', 'reference', 'default_question']
        #fields = ['CompanyName', 'CompanyURL']

class BookModelForm(BSModalForm):
    class Meta:
        model = FrameworkControls
        fields = ['framework', 'function', 'category', 'subcategoryID', 'subcategory', 'reference', 'default_question']

class FrameworkControlsModifyForm(forms.Form):
    class Meta:
        model = FrameworkControls

#class NewFrameworkForm(BSModalForm):
class NewFrameworkForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '75'}))
    short_name = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}))
    version = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}))
    #publication_date = forms.DateTimeField(

    #    input_formats=['%d/%m/%Y %H:%M'],
    #    widget=BootstrapDateTimePickerInput()
    #    )
    source = forms.ModelChoiceField(FrameworkSource.objects.all(), widget=BootstrapSelect())
    class Meta:
        model = Framework
        #exclude = ['id']
        fields = ['name', 'short_name', 'version', 'publication_date', 'source']
        widgets = {
            'publication_date': DatePicker(
                options={
                    'format': 'MM/DD/YYYY'
                },
                attrs={
                    'append': 'fa fa-calendar',
                },
            )
        }

    def __init__(self, *args, **kwargs):
        super(NewFrameworkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-8 mb-0'),

                css_class='form-row'
            ),
            Row(
                #Column('city', css_class='form-group col-md-6 mb-0'),
                #Column('state', css_class='form-group col-md-4 mb-0'),
                #Column('zip_code', css_class='form-group col-md-2 mb-0'),
                Column('version', css_class='form-group col-md-4 mb-0'),
                Column('short_name', css_class='form-group col-md-4 mb-0'),
                Column('publication_date', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('source', css_class='form-group col-md-6 mb-0'),

            ),
            #Submit('submit', 'Create Assessment')
        )
        self.helper.add_input(Submit('submit', 'Create Framework'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )
        self.helper.add_input(Submit(
            'AddSource',
            'Add Framework Source',
            css_class='btn-secondary',
            formnovalidate='formnovalidate',
            )
        )


class NewFrameworkSourceForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '75'}))
    url = forms.CharField(widget=forms.TextInput(attrs={'size': '75'}))
    acronym = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}))

    #publication_date = forms.DateTimeField(

    #    input_formats=['%d/%m/%Y %H:%M'],
    #    widget=BootstrapDateTimePickerInput()
    #    )

    class Meta:
        model = FrameworkSource
        #exclude = ['id']
        fields = ['name', 'acronym', 'url', ]


    def __init__(self, *args, **kwargs):
        super(NewFrameworkSourceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-8 mb-0'),

                css_class='form-row'
            ),
            Row(
                #Column('city', css_class='form-group col-md-6 mb-0'),
                #Column('state', css_class='form-group col-md-4 mb-0'),
                #Column('zip_code', css_class='form-group col-md-2 mb-0'),
                Column('url', css_class='form-group col-md-8 mb-0'),

                css_class='form-row'
            ),
            Row(
                Column('acronym', css_class='form-group col-md-6 mb-0'),

            ),
            #Submit('submit', 'Create Assessment')
        )
        self.helper.add_input(Submit('submit', 'Create Framework Source'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )


###Questionnaire Forms
#VendorContactQuestionnaireForm
class VendorContactQuestionnaireForm(forms.Form):
    #if self.user.groups.filter(name = u"vendor").exists():
    #    control = forms.CharField(widget=forms.Textarea)
    #    question = forms.CharField(widget=forms.Textarea)
    #    answer = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    #elif self.user.groups.filter(name = u"analyst").exists():
    control = forms.CharField(widget=forms.Textarea)
    question = forms.CharField(widget=forms.Textarea)
    answer = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    notes = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))

    class Meta:
        model = Question
        fields = []
        fields = ['control', 'question', 'answer', ]

    #def __init__(self, *args, **kwargs):
    #    self.user = kwargs.pop('user',None)
    #    if self.user.groups.filter(name = u"analyst").exists():
    #        self.fields = ['control', 'question', 'answer', 'compliance', 'notes', 'likelihood', 'impact', 'risk_rating']
    #    elif self.user.groups.filter(name = u"analyst").exists():
    #        self.fields = [ 'control', 'question', 'answer', ]
    #    super(VendorContactQuesitonnaireForm, self).__init__(*args, **kwargs)

class AnalysisQuestionnaireForm(forms.Form):
    control = forms.CharField(widget=forms.Textarea)
    question = forms.CharField(widget=forms.Textarea)
    answer = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    notes = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    #answer = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))

    class Meta:
        model = Question
        fields = ['control', 'question', 'answer', 'compliance', 'notes', 'likelihood', 'impact', 'risk_rating']

    def __init__(self, *args, **kwargs):
        super(AnalysisQuestionnaireForm, self).__init__(*args, **kwargs)
        self.fields['control'].widget.attrs['readonly'] = True # text input
        self.fields['question'].widget.attrs['readonly'] = True # text input
        self.fields['answer'].widget.attrs['readonly'] = True # text input

#AnalystQuestionnaireForm
class AnalystQuestionnaireForm(forms.Form):
    class Meta:
        model = Questionnaire
        fields = ['assessment', 'question_framework', 'question', 'answer', 'compliance', 'notes', 'likelihood', 'impact', 'risk_rating']

    def __init__(self, *args, **kwargs):
        super(AnalystContactQuestionnaireForm, self).__init__(*args, **kwargs)
        self.fields['control'].widget.attrs['readonly'] = True # text input
        self.fields['question'].widget.attrs['readonly'] = True # text input
        self.fields['question_framework'].widget.attrs['readonly'] = True # text input
        self.fields['question'].widget.attrs['readonly'] = True # text input
        self.fields['answer'].widget.attrs['readonly'] = True # text input


class AssessmentFrameworkChangeListForm(forms.ModelForm):
    # here we only need to define the field we want to be editable
    framework = forms.ModelMultipleChoiceField(
        queryset=Framework.objects.all(), required=False)

class CreateQuestionsForm(forms.Form):
    #def __init__(self, *args, **kwargs):
    #    self.request = kwargs.pop('uuid', None)
    #    super(CreateQuestionsForm, self).__init__(*args, **kwargs)

    def PopulateQuestions(self, uuid):
        #passed uuid is assessment uuid
        # look up quesitonnaire containing assessment uuid
        #uuid = self.kwargs['uuid']
    #    uuid = self.request.uuid
    #    print("UUID passed: " + str(self.request.uuid))

        questionnaire = Questionnaire.objects.filter(assessment=uuid).first()
        aframework_set = AssessmentFrameworks.objects.filter(assessment=uuid)

        for afwork in aframework_set:
            #print("Processing framework:" + str(afwork.framework.name))
            controls_set = FrameworkControls.objects.filter(framework=afwork.framework)
            for ctrl in controls_set:
                print("Processing control: " + ctrl.categoryID)
                NewQuestion = Question()
                NewQuestion.questionnaire = questionnaire
                NewQuestion.assessment = questionnaire.assessment
                NewQuestion.control = ctrl
                NewQuestion.question = ctrl.default_question
                #NewQuestion.answer = ""
                #NewQuestion.compliance = ""
                #NewQuestion.notes = ""
                #NewQuestion.likelihood = ""
                #NewQuestion.impact = ""
                #NewQuestion.risk_rating = ""
                NewQuestion.save()

class QuestionEditForm(forms.ModelForm):
    #control = forms.CharField(required=False, widget=forms.HiddenInput())
    question = forms.CharField(required=False, widget=forms.Textarea())

    class Meta:
        model = Question
        fields = [ 'control', 'question']

class NewAnswerForm(forms.ModelForm):
    #questionnaire = forms.CharField(required=False, widget=forms.HiddenInput())
    #assessment = forms.CharField(required=False, widget=forms.HiddenInput())
    #control = forms.CharField(required=False, widget=forms.HiddenInput())
    #question = forms.CharField(required=False, widget=forms.HiddenInput())
    #compliance = forms.CharField(required=False, widget=forms.HiddenInput())
    #notes = forms.CharField(required=False, widget=forms.HiddenInput())
    #likelihood = forms.CharField(required=False, widget=forms.HiddenInput())
    #impact = forms.CharField(required=False, widget=forms.HiddenInput())
    #risk_rating = forms.CharField(required=False, widget=forms.HiddenInput())
    answer  = forms.CharField(widget=forms.Textarea())
    #passed_quuid   = forms.CharField(widget=forms.HiddenInput())
    next = forms.UUIDField()

    class Meta:
        model = Question
        #exclude = ['id']
        #fields = [ 'question', 'answer' ]
        fields = [ 'answer' ] #, 'questionnaire', 'assessment', 'control', 'question', 'answer', 'compliance', 'notes', 'likelihood', 'impact', 'risk_rating' ]

        #def clean(self):
        #    cleaned_data = super(NewAnswerForm, self).clean()
        #    quuid = cleaned_data['passed_quuid']
            #start = cleaned_data['t_start']
            #end = cleaned_data['t_end']
        #    answer = cleand_data['answer']
        #    conflicts = Questions.objects.filter(
        #        		=office_id,
        #        		t_start__lte=end,
        #        		t_end__gte=start
        #            ).exclude(pk=self.instance.id)
        #    if any(conflicts):
        #        raise forms.ValidationError("There's conflicts with another reservations between those dates.")

        #    return cleaned_data

    #widgets = { 'answer': forms.Textarea(),
        #            'questionnaire': forms.HiddenInput(),
        #            'assessment': forms.HiddenInput(),
        #            'control': forms.HiddenInput(),
        #            'question': forms.HiddenInput(),
        #            'compliance': forms.HiddenInput(),
        #            'notes': forms.HiddenInput(),
        #            'likelihood': forms.HiddenInput(),
        #            'impact': forms.HiddenInput(),
        #            'risk_rating': forms.HiddenInput(),
        #            }
#    def PopulateAnswer(self, uuid):
#        print("UUID passed to PopulateAnswer is: " + str(uuid))
#        answered_question = Questions.objects.filter(uuid=uuid).first()
#        answered_question.answer = self.answer
#
#        answered_question.save()

    #def PopulateAnswer(self):
    #    print("PopulateAnswer was hit ...")
    #    pass


class NewAnalysisForm(forms.ModelForm):
    #answer  = forms.CharField(widget=forms.Textarea())
    #compliance  =   forms.CharField(max_length=1000,required=False)

    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )
    answer      = forms.CharField()
    question    = forms.CharField()
    compliance  = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Compliant / Not Compliant",
                              initial='True', widget=forms.Select(), required=False)
    notes       = forms.CharField(max_length=1000,required=False)
    LIKELIHOOD_CHOICES = [ ('VERY_LOW', 'Very Low'), ('LOW', 'Low'), ('MODERATE', 'Moderate'), ('HIGH', 'High'), ('VERY_HIGH', 'Very High') ]
    likelihood  = forms.ChoiceField(choices=LIKELIHOOD_CHOICES, label="Likelihood of Exploit", required=False)
    IMPACT_CHOICES = [ ('VERY_LOW', 'Very Low'), ('LOW', 'Low'), ('MODERATE', 'Moderate'), ('HIGH', 'High'), ('VERY_HIGH', 'Very High') ]
    impact      = forms.ChoiceField(choices=IMPACT_CHOICES, label="Impact", required=False)
    RISK_CHOICES = [ ('VERY_LOW', 'Very Low'), ('LOW', 'Low'), ('MODERATE', 'Moderate'), ('HIGH', 'High'), ('VERY_HIGH', 'Very High') ]
    risk_rating = forms.ChoiceField(choices=RISK_CHOICES, label="risk_rating", required=False)
    was_analyzed = forms.BooleanField(required=False)
    next        = forms.UUIDField()

    class Meta:
        model = Question
        fields = [ 'question', 'answer', 'compliance', 'notes', 'likelihood', 'impact', 'risk_rating', 'was_analyzed' ]

    def __init__(self, *args, **kwargs):
        super(NewAnalysisForm, self).__init__(*args, **kwargs)
        self.fields['question'].widget.attrs['readonly'] = True
        self.fields['answer'].widget.attrs['readonly'] = True
        self.fields['risk_rating'].widget.attrs['readonly'] = True

class NewAnalysisForm2(forms.ModelForm):
    #answer  = forms.CharField(widget=forms.Textarea())
    #compliance  =   forms.CharField(max_length=1000,required=False)

    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )
    answer      = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 70}), required=False)
    question    = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 70}), required=False)
    compliance  = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Compliant / Not Compliant",
                              initial='True', widget=forms.Select(), required=False)
    notes       = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 70}), required=False)
    LIKELIHOOD_CHOICES = [ ('VERY_LOW', 'Very Low'), ('LOW', 'Low'), ('MODERATE', 'Moderate'), ('HIGH', 'High'), ('VERY_HIGH', 'Very High') ]
    likelihood  = forms.ChoiceField(choices=LIKELIHOOD_CHOICES, label="Likelihood of Exploit", required=False, widget=forms.Select(attrs = {'onchange' : "calcRisk();"}))
    IMPACT_CHOICES = [ ('VERY_LOW', 'Very Low'), ('LOW', 'Low'), ('MODERATE', 'Moderate'), ('HIGH', 'High'), ('VERY_HIGH', 'Very High') ]
    impact      = forms.ChoiceField(choices=IMPACT_CHOICES, label="Impact", required=False, widget=forms.Select(attrs = {'onchange' : "calcRisk();"}))
    RISK_CHOICES = [ ('VERY_LOW', 'Very Low'), ('LOW', 'Low'), ('MODERATE', 'Moderate'), ('HIGH', 'High'), ('VERY_HIGH', 'Very High') ]
    risk_rating = forms.ChoiceField(choices=RISK_CHOICES, label="risk_rating", required=False)
    #risk_rating = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 10}))
    was_analyzed = forms.BooleanField(required=False)
    next        = forms.UUIDField()

    class Meta:
        model = Question
        fields = [ 'question', 'answer', 'compliance', 'notes', 'likelihood', 'impact', 'risk_rating', 'was_analyzed' ]

    def __init__(self, *args, **kwargs):
        super(NewAnalysisForm2, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.fields['question'].widget.attrs['readonly'] = True
        self.fields['answer'].widget.attrs['readonly'] = True
        self.helper.layout = Layout(
            Row(
                Column('question', css_class='form-group col-lg-8 mb-0'),

                css_class='form-row'
            ),
            Row(
                #Column('city', css_class='form-group col-md-6 mb-0'),
                #Column('state', css_class='form-group col-md-4 mb-0'),
                #Column('zip_code', css_class='form-group col-md-2 mb-0'),

                Column('answer', css_class='form-group col-xl'),

                css_class='form-row'
            ),
            Row(
                Column('compliance', css_class='form-group col-md-6 mb-0'),


            ),
            Row(
                Column('notes', css_class='form-group col-md-6 mb-0'),


            ),
            Row(
                Column('likelihood', css_class='form-group col-md-6 mb-0'),
                Column('impact', css_class='form-group col-md-6 mb-0'),
                Column('risk_rating', css_class='form-group col-md-6 mb-0'),


            ),
            #Submit('submit', 'Create Assessment')
        )
        self.helper.add_input(Submit('submit', 'Complete Analysis'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )


class CreateReportForm(forms.Form):

    def PopulateQuestions(self, uuid):

        questionnaire = Questionnaire.objects.filter(assessment=uuid).first()
        aframework_set = AssessmentFrameworks.objects.filter(assessment=uuid)

        for afwork in aframework_set:
            #print("Processing framework:" + str(afwork.framework.name))
            controls_set = FrameworkControls.objects.filter(framework=afwork.framework)
            for ctrl in controls_set:
                #print("Processing control: " + ctrl.categoryID)
                NewQuestion = Question()
                NewQuestion.questionnaire = questionnaire
                NewQuestion.assessment = questionnaire.assessment
                NewQuestion.control = ctrl
                NewQuestion.question = ctrl.default_question
                #NewQuestion.answer = ""
                #NewQuestion.compliance = ""
                #NewQuestion.notes = ""
                #NewQuestion.likelihood = ""
                #NewQuestion.impact = ""
                #NewQuestion.risk_rating = ""
                NewQuestion.save()


class UpdateFrameworkForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '75'}))
    short_name = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}))
    version = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}))
    #publication_date = forms.DateTimeField(
    #    input_formats=['%d/%m/%Y'],
    #    widget=BootstrapDateTimePickerInput()
    #    )
    source = forms.ModelChoiceField(FrameworkSource.objects.all())
    class Meta:
        model = Framework
        #exclude = ['id']
        fields = ['name', 'short_name', 'version', 'publication_date', 'source']
        widgets = {
            'publication_date': DatePicker(
                options={
                    'format': 'MM/DD/YYYY'
                },
                attrs={
                    'prepend': 'fa fa-calendar',
                },
            )
        }

    def __init__(self, *args, **kwargs):
        super(UpdateFrameworkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-8 mb-0'),

                css_class='form-row'
            ),
            Row(
                #Column('city', css_class='form-group col-md-6 mb-0'),
                #Column('state', css_class='form-group col-md-4 mb-0'),
                #Column('zip_code', css_class='form-group col-md-2 mb-0'),
                Column('version', css_class='form-group col-md-4 mb-0'),
                Column('short_name', css_class='form-group col-md-4 mb-0'),
                Column('publication_date', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('source', css_class='form-group col-md-6 mb-0')
            ),
            #Submit('submit', 'Create Assessment')
        )
        self.helper.add_input(Submit('submit', 'Update Framework'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )
        self.helper.add_input(Submit(
            'AddControls',
            'Add Controls to Framework',
            css_class='btn-secondary',
            formnovalidate='formnovalidate',
            )
        )




class UpdateAssessmentForm(forms.ModelForm):
    STATUS_CHOICES = [ ('CREATED', 'Created'),
        ('QUESTIONNAIRE_REVIEW', 'Questionnaire in Review'),
        ('VENDOR_SUBMIT', 'Submitted to Vendor'),
        ('IN_ANALYSIS', 'In Analysis'),
        ('REPORT_GENERATED', 'Report Generated'),
        ('ASSESSMENT_REVIEW', 'Assessment Under Review'),
        ('ASSESSMENT_COMPLETE', 'Assessment Complete'),]
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '75'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, disabled=True)
    #vendor = forms.ModelChoiceField(queryset=Company.objects.all())
    vendor = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=autocomplete.ModelSelect2(url='company-autocomplete'),
        label="Company"
    )
    vendor_contact = forms.ModelChoiceField(queryset=User.objects.all(), widget=BootstrapSelect())
    owner = forms.ModelChoiceField(User.objects.all(),required=False, widget=BootstrapSelect())
    auditor = forms.ModelChoiceField(User.objects.all(),required=False, widget=BootstrapSelect())
    analyst = forms.ModelChoiceField(User.objects.all(),required=False, widget=BootstrapSelect())
    #start_date = forms.DateTimeField(
    #    input_formats=['%d/%m/%Y %H:%M'],
    #    widget=BootstrapDateTimePickerInput()
    #    )


    class Meta:
        model = Assessment
        #exclude = ['id']
        fields = [ 'name', 'vendor', 'owner', 'vendor_contact', 'start_date','status', 'auditor', 'analyst', 'frameworks' ]
        widgets = {
            'start_date': DatePicker(
                options={
                    'format': 'MM/DD/YYYY'
                },
                attrs={
                    'append': 'fa fa-calendar',
                },
            )
        }

    def __init__(self, *args, **kwargs):
        super(UpdateAssessmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-8 mb-0'),

                css_class='form-row'
            ),
            Row(
                #Column('city', css_class='form-group col-md-6 mb-0'),
                #Column('state', css_class='form-group col-md-4 mb-0'),
                #Column('zip_code', css_class='form-group col-md-2 mb-0'),
                Column('status', css_class='form-group col-md-4 mb-0'),
                Column('vendor', css_class='form-group col-md-4 mb-0'),
                Column('vendor_contact', css_class='form-group col-md-4 mb-0'),

                css_class='form-row'
            ),
            Row(

                Column('owner', css_class='form-group col-md-4 mb-0'),
                Column('analyst', css_class='form-group col-md-4 mb-0'),
                Column('start_date', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('frameworks', css_class='form-group col-md-6 mb-0')
            ),
            #Submit('submit', 'Create Assessment')
        )
        self.helper.add_input(Submit('submit', 'Update Assessment'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )
        self.fields["frameworks"].widget = CheckboxSelectMultiple()
        self.fields["frameworks"].queryset = Framework.objects.all()

class CreateReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(CreateReportForm, self).__init__(*args, **kwargs)

    def GenerateReport(self, uuid, user):
        questionnaire = Questionnaire.objects.filter(assessment=uuid).first()
        assessment = Assessment.objects.filter(uuid=uuid).first()


        NewReport = Report()
        NewReport.name = assessment.name + " Report"
        NewReport.publication_date = datetime.date.today()
        NewReport.questionnaire = questionnaire
        NewReport.assessment = assessment
        NewReport.executive_summary = ""
        NewReport.executive_compliance_summary = ""
        NewReport.executive_risk_assessment_summary = ""
        NewReport.nc_controls = 0
        NewReport.c_controls = 0
        NewReport.author = user
        NewReport.save()


class UpdateFrameworkControlsForm(forms.ModelForm):
    function = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))
    functionID = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '25'}))
    category = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))
    categoryID = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '25'}), label="Category ID")
    category_statement = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '75'}))
    subcategory = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '50'}))
    subcategoryID = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '25'}), label="SubCategory ID")
    category_statement = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '75'}))
    default_question = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '75'}))

    #we should add an author field and populate it on save with the user's UUIDField
    #we should add a create_date field and populate it on new/create
    #we should add a modified date field and populate it on save with today's date


    class Meta:
        model = FrameworkControls
        #exclude = ['id']
        fields = [ 'function', 'functionID', 'category', 'categoryID', 'category_statement', 'subcategory', 'subcategoryID', 'control_statement', 'default_question', 'reference' ]
        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super(UpdateFrameworkControlsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("""
                <div class="layout-subheader">Control Categorization</div>
                <p>
                <hr>
            """),
            Row(
                Column('function', css_class='form-group col-md-6 mb-0'),
                Column('category', css_class='form-group col-md-4 mb-0'),
                Column('categoryID', css_class='form-group col-md-4 mb-0'),
                #Column('functionID', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('category_statement', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                    #Column('city', css_class='form-group col-md-6 mb-0'),
                    #Column('state', css_class='form-group col-md-4 mb-0'),
                    #Column('zip_code', css_class='form-group col-md-2 mb-0'),
                    Column('subcategory', css_class='form-group col-md-4 mb-0'),
                    Column('subcategoryID', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
            ),
            HTML("""
                <p>
                <hr>
                <p>
                <div class="layout-subheader">Control Content</div>
                <p>
                <hr>
            """),
            Row(
                Column('control_statement', css_class='form-group col-md-8 mb-0'),
            ),
            Row(
                Column('default_question', css_class='form-group col-md-8 mb-0'),
            ),
            Row(
                Column('reference', css_class='form-group col-md-8 mb-0'),

            ),

            #Submit('submit', 'Create Assessment')
        )
        self.helper.add_input(Submit('submit', 'Update Control'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )

class CreateFrameworkControlsForm(forms.ModelForm):

    framework = forms.CharField(label="Framework")
    function = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    functionID = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}))
    category = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    categoryID = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}), label="Category ID")
    category_statement = forms.CharField(widget=forms.TextInput(attrs={'size': '75'}))
    subcategory = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    subcategoryID = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}), label="SubCategory ID")
    category_statement = forms.CharField(widget=forms.TextInput(attrs={'size': '75'}))
    default_question = forms.CharField(widget=forms.TextInput(attrs={'size': '75'}))

    #we should add an author field and populate it on save with the user's UUIDField
    #we should add a create_date field and populate it on new/create
    #we should add a modified date field and populate it on save with today's date


    class Meta:
        model = FrameworkControls
        #exclude = ['id']
        fields = [ 'framework', 'function', 'functionID', 'category', 'categoryID', 'category_statement', 'subcategory', 'subcategoryID', 'control_statement', 'default_question', 'reference' ]
        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super(UpdateFrameworkControlsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("""
                <div class="layout-subheader">Control Categorization</div>
                <p>
                <hr>
            """),
            Row(
                Column('function', css_class='form-group col-md-6 mb-0'),
                Column('category', css_class='form-group col-md-4 mb-0'),
                Column('categoryID', css_class='form-group col-md-4 mb-0'),
                #Column('functionID', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('category_statement', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                    #Column('city', css_class='form-group col-md-6 mb-0'),
                    #Column('state', css_class='form-group col-md-4 mb-0'),
                    #Column('zip_code', css_class='form-group col-md-2 mb-0'),
                    Column('subcategory', css_class='form-group col-md-4 mb-0'),
                    Column('subcategoryID', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
            ),
            HTML("""
                <p>
                <hr>
                <p>
                <div class="layout-subheader">Control Content</div>
                <p>
                <hr>
            """),
            Row(
                Column('control_statement', css_class='form-group col-md-8 mb-0'),
            ),
            Row(
                Column('default_question', css_class='form-group col-md-8 mb-0'),
            ),
            Row(
                Column('reference', css_class='form-group col-md-8 mb-0'),

            ),

            #Submit('submit', 'Create Assessment')
        )
        self.helper.add_input(Submit('submit', 'Update Control'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )

class Add2FWFrameworkControlsForm(forms.ModelForm):

    #framework = forms.CharField(label="Framework")
    framework = forms.ModelChoiceField(Framework.objects.all(), widget=BootstrapSelect())
    frameworkUUID = forms.CharField(widget=forms.TextInput(attrs={'size': '100'}), disabled=True)
    function = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    #functionID = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}))
    category = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    categoryID = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}), label="Category ID")
    category_statement = forms.CharField(widget=forms.TextInput(attrs={'size': '75'}))
    subcategory = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    subcategoryID = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}), label="SubCategory ID")
    category_statement = forms.CharField(widget=forms.TextInput(attrs={'size': '75'}))
    default_question = forms.CharField(widget=forms.TextInput(attrs={'size': '75'}))

    #we should add an author field and populate it on save with the user's UUIDField
    #we should add a create_date field and populate it on new/create
    #we should add a modified date field and populate it on save with today's date


    class Meta:
        model = FrameworkControls
        #exclude = ['id']
        fields = [ 'framework', 'function', 'frameworkUUID', 'category', 'categoryID', 'category_statement', 'subcategory', 'subcategoryID', 'control_statement', 'default_question', 'reference' ]
        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super(Add2FWFrameworkControlsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('framework', css_class='form-group col-md-8 mb-0'),
                Field('frameworkUUID', type="hidden"),
                css_class='form-row'
            ),
            HTML("""
                <div class="layout-subheader">Control Categorization</div>
                <p>
                <hr>

            """),
            #HTML(
            #    "<input type='hidden id='frameworkUUID' name='frameworkUUID' value='" + str(kwargs['uuid']) + "'>"
            #),
            Row(
                Column('function', css_class='form-group col-md-6 mb-0'),
                Column('category', css_class='form-group col-md-4 mb-0'),
                Column('categoryID', css_class='form-group col-md-4 mb-0'),
                #Column('functionID', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('category_statement', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                    #Column('city', css_class='form-group col-md-6 mb-0'),
                    #Column('state', css_class='form-group col-md-4 mb-0'),
                    #Column('zip_code', css_class='form-group col-md-2 mb-0'),
                    Column('subcategory', css_class='form-group col-md-4 mb-0'),
                    Column('subcategoryID', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
            ),
            HTML("""
                <p>
                <hr>
                <p>
                <div class="layout-subheader">Control Content</div>
                <p>
                <hr>
            """),
            Row(
                Column('control_statement', css_class='form-group col-md-8 mb-0'),
            ),
            Row(
                Column('default_question', css_class='form-group col-md-8 mb-0'),
            ),
            Row(
                Column('reference', css_class='form-group col-md-8 mb-0'),

            ),

            #Submit('submit', 'Create Assessment')
        )
        self.helper.add_input(Submit('submit', 'Create Control'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )




class AddMulti2FWFrameworkControlsForm(forms.Form):
    #static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #model = Framework
    #class Meta:
    #    model = Framework
    #    fields = [ 'controls_file' ]
    #framework = forms.CharField(label="Framework", disabled=True)
    controls_file = forms.FileField(
        label='Upload a CSV File containing controls ...',

        #help_text='max. 42 megabytes'
    )
    def __init__(self, *args, **kwargs):
        super(AddMulti2FWFrameworkControlsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                #Column('framework', css_class='form-group col-md-8 mb-0'),
                Column('controls_file', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

            #Submit('submit', 'Create Assessment')
        )
        self.helper.add_input(Submit('submit', 'Upload Controls'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )



class AssessmentListForm(forms.Form):
    class Meta:
        model = Assessment
        fields = [ 'name', 'vendor', 'owner', 'status', 'frameworks' ]

#class AssessmentDetailForm(forms.Form):
#    class Meta:
#        model = Assessment
#        fields = [ 'name', 'vendor', 'owner', 'vendor_contact', 'auditor', 'analyst', 'status', 'frameworks' ]
#        #fields = ['CompanyName', 'CompanyURL']

class AnswerUpdateForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = [
            'answer',
        ]

class ReportUpdateForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = [
            'executive_summary',
            'executive_findings',
            'executive_compliance_summary',
            'executive_risk_assessment_summary',
            'executive_compliance_chart',
            'executive_risk_chart',
            #'nc_controls',
            #'c_controls',
        ]

class ReportGenForm(forms.Form):
        model = Report
        fields = [
            'executive_summary',
            'executive_findings',
            'executive_compliance_summary',
            'executive_risk_assessment_summary',
            'executive_compliance_chart',
            'executive_risk_chart',
            #'nc_controls',
            #'c_controls',
        ]


class AssessmentStatusForm(forms.ModelForm):

    #name = forms.CharField(widget=forms.TextInput(),disabled=True)
    status = forms.CharField(disabled=True)
    #vendor = forms.ModelChoiceField(queryset=Company.objects.all())
    vendor = forms.CharField(
        label="Vendor",
        disabled=True
    )
    vendor_contact = forms.CharField(disabled=True)

    class Meta:
        model = Assessment
        #exclude = ['id']
        fields = [ 'name', 'vendor', 'owner', 'vendor_contact', 'start_date', 'auditor', 'analyst', 'status', 'frameworks' ]

    def __init__(self, *args, **kwargs):
        super(AssessmentStatusForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                HTML(
                    '''
                    {% if assessment.status == "CREATED" %}
                        Assessment Progress
                        <div class="progress">
                          <div class="progress-bar bg-success" role="progressbar" style="width: 10%;" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100">10%</div>
                        </div>
                    {% elif assessment.status == "SUBMITTED_TO_VENDOR" %}
                        Assessment Progress
                        <div class="progress">
                          <div class="progress-bar bg-success" role="progressbar" style="width: 25%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">25%</div>
                        </div>
                    {% elif assessment.status == "SUBMITTED_FOR_ANALYSIS" %}
                        Assessment Progress
                        <div class="progress">
                          <div class="progress-bar bg-success" role="progressbar" style="width: 50%;" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">50%</div>
                        </div>
                    {% elif assessment.status == "ANALYSIS_COMPLETE" %}
                        Assessment Progress
                        <div class="progress">
                          <div class="progress-bar bg-success" role="progressbar" style="width: 75%;" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">75%</div>
                        </div>
                    {% elif assessment.status == "REPORT_GENERATED" %}
                        Assessment Progress
                        <div class="progress">
                          <div class="progress-bar bg-success" role="progressbar" style="width: 100%;" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">100%</div>
                        </div>
                    {% endif %}
                    <p>
                    <div class="assessment-subheader"><h5>Vendor & Frameworks</h5></div>
                    <p>
                    <hr>
                    <p>
                    <div class="form-row " >
                      <div  class="col form-group col-md-6 mb-0" >
                        <div id="div_id_vendor" class="form-group">
                          <label for="id_vendor" class=" requiredField">
                            Vendor:
                            <span class="asteriskField">*</span>
                          </label>
                          <div class="">
                            <input type="text" name="vendor" value="{{ assessment.vendor.name }}" class="textinput textInput form-control" required disabled id="id_vendor">
                          </div> <!-- close vendor name -->
                         </div>  <!-- close div_id_vendor -->
                       </div> <!-- close column -->
 & Statu
                    '''
                    ),
                Column('frameworks', css_class='form-group col-md-6 mb-0'),
                HTML(
                    '''
                      </div><!-- close row -->
                    '''
                    ),
                HTML(
                        '''
                        <p>
                        <p>
                        <hr>
                        <div class="assessment-subheader"><h5>Assign Vendor Point of Contact</h5></div>
                        <p>
                        <hr>
                        <p>
                        <div class="form-row " >
                          <div  class="col form-group col-md-6 mb-0" >
                            <div id="div_id_vendor_contact" class="form-group">
                              <label for="id_vendor_contact" class=" requiredField">
                                Vendor PoC Name:
                                <span class="asteriskField">*</span>
                              </label>
                              <div class="">
                                <input type="text" name="vendor_contact" value="{{ assessment.vendor_contact.first_name }} {{ assessment.vendor_contact.last_name }} " class="textinput textInput form-control" required disabled id="id_vendor_contact">
                              </div> <!-- close vendor_contact name -->
                             </div>  <!-- close div_id_vendor -->
                           </div> <!-- close column -->

                        '''
                    ),
                    #Column('status', css_class='form-group col-md-4 mb-0'),
                    HTML(
                        '''
                        </div><!-- close row -->
                            <div class="form-row " >
                              <div  class="col form-group col-md-6 mb-0" >
                              {% if assessment.status == "CREATED" %}

                                <div class="">
                                    <button type="button" class="btn btn-secondary" formnovalidate="formnovalidate">Assessment Started</button>
                                </div>
                            {% else %}

                                <div class="">
                                    <a href=""><input type="submit" name="start_assessment" value="Start Assessment" class="btn btn-primary btn-primary" id="submit-id-cancel" formnovalidate="formnovalidate"/></a>
                                </div>
                              {% endif %}
                              </div> <!-- close col -->
                          </div><!-- close row -->
                        '''
                        ),
                        HTML(
                                '''
                                <p>
                                <p>
                                <hr>
                                <div class="assessment-subheader"><h5>Analyst</h5></div>
                                <p>
                                <hr>
                                <p>
                                <div class="form-row " >
                                  <div  class="col form-group col-md-6 mb-0" >
                                    <div id="div_id_analyst" class="form-group">
                                      <label for="id_analyst" class=" requiredField">
                                        Analyst:
                                        <span class="asteriskField">*</span>
                                      </label>
                                      <div class="">
                                        <input type="text" name="analyst" value="{{ assessment.analyst.first_name }} {{ assessment.analyst.last_name }} " class="textinput textInput form-control" required disabled id="id_analyst">
                                      </div> <!-- close analyst name -->
                                     </div>  <!-- close div_id_analyst -->
                                   </div> <!-- close column -->

                                '''
                            ),
                            HTML(
                                '''
                                </div><!-- close row -->
                                    <div class="form-row " >
                                      <div  class="col form-group col-md-6 mb-0" >
                                      {% if assessment.status != "SUBMITTED_FOR_ANALYSIS" %}

                                        <div class="">
                                            <button type="button" class="btn btn-secondary"  formnovalidate="formnovalidate">Questionnaire Analyzed</button>
                                        </div>
                                    {% else %}

                                        <div class="">
                                            <a href=""><input type="submit" name="start_assessment" value="Start Assessment" class="btn btn-primary btn-primary" id="submit-id-cancel" formnovalidate="formnovalidate"/></a>
                                        </div>
                                      {% endif %}
                                      </div> <!-- close col -->
                                  </div><!-- close row -->
                                '''
                                ),
            )
        self.helper.add_input(Submit('submit', 'Update Assessment'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )
        self.fields["frameworks"].widget = CheckboxSelectMultiple()
        self.fields["frameworks"].queryset = Framework.objects.all()


#class AssessmentModifyForm(forms.Form):
class AssessmentModifyForm(forms.Form):
    #Vendor = forms.ModelChoiceField(queryset=Vendor.objects.all())
    class Meta:
        model = Assessment
        #fields = '__all__'
        fields = [ 'name', 'vendor', 'owner', 'vendor_contact', 'auditor', 'analyst', 'status', 'frameworks' ]

class AnswerDocumentUpdateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'document',
            'name',
            'description'
        ]

class BSModAnswerDocumentUpdateForm(BSModalModelForm):
    class Meta:
        model = Document
        fields = [
            'document',
            'name',
            'description'
        ]

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields =['document']


#class ConfigForm(forms.Form):
#    configfile = forms.FileField(
#        label='Upload a Configuration File',
#        #help_text='max. 42 megabytes'
#    )
