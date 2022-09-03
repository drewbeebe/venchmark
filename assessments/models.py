import datetime
import uuid
from itertools import chain

#imports for django
from django.db import models
from django.db.models import F, Q # new
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, validate_email
from django.core.files.storage import FileSystemStorage

from django.conf import settings
from django.conf.urls.static import static

from django.db.models.signals import post_save
from django.dispatch import receiver

#imports from app models
from companies.models import Company, User
from .managers import FrameworkManager, FrameworkSourceManager, FrameworkControlsManager, AssessmentManager, QuestionManager  #, QuestionnaireManager

#local imports
from . risks import CalcRiskRating




##### 2020-04-05 - DB - migrating Frameworks models over to Assessments to help with Through Tables
# Create your models here.
class FrameworkSource(models.Model):
    # fields
    #orderID = models.IntegerField(primary_key=True, null=False, editable=False, unique=True)
    order_id = models.IntegerField(default=1)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this Framework Source.', editable=False, unique=True)
    name = models.CharField(max_length=50, default='', help_text="Enter the Source's First Name")
    acronym = models.CharField(max_length=14, default='', help_text="Enter the Source's Acronym")
    url = models.CharField(max_length=200, default='', help_text="Enter the Source's Web Site URL")
    #SourceID = models.ForeignKey(Source, , on_delete=models.CASCADE)
    objects = FrameworkSourceManager()
    # Metadata
    class Meta:
        ordering = ['order_id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = FrameworkSource.objects.all().aggregate(largest=models.Max('order_id'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.order_id = last_id + 1
        super(FrameworkSource, self).save(*args, **kwargs)




class Framework(models.Model):
    def framework_based_upload_to(instance, filename):
        return "uploads/{}/{}".format(instance.uuid, filename)

    # fields
    #upload_storage = FileSystemStorage(settings.UPLOAD_DIRS)
    #orderID = models.IntegerField(primary_key=True, null=False, editable=False, unique=True)
    order_id = models.IntegerField(default=1)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this Framework.', editable=False, unique=True)
    name = models.CharField(max_length=200, default='', help_text="Enter the Framework's First Name")
    short_name = models.CharField(max_length=50, default='', help_text="Enter the Framework's First Name")
    version = models.CharField(max_length=3, default='1.1', help_text="Enter the Framework's Version Number")
    publication_date = models.DateField(default=datetime.date.today, help_text="Enter the date the framework was published")
    assessments = models.ManyToManyField('Assessment', through='AssessmentFrameworks')
    source = models.ForeignKey(FrameworkSource, related_name='+', on_delete=models.CASCADE)
    controls_file = models.FileField(upload_to=framework_based_upload_to, blank=True)

    objects = FrameworkManager()
    # Metadata
    class Meta:
        ordering = ['order_id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = Framework.objects.all().aggregate(largest=models.Max('order_id'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.order_id = last_id + 1
        super(Framework, self).save(*args, **kwargs)

class FrameworkControls(models.Model):

    # fields
    #orderID = models.IntegerField(primary_key=True, null=False, editable=False, unique=True)
    order_id = models.IntegerField(default=1)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this Framework Control.', editable=False, unique=True)
    framework = models.ForeignKey(Framework, related_name='+', on_delete=models.CASCADE)
    frameworkUUID = models.UUIDField(primary_key=False)
    function = models.CharField(max_length=50, default='', help_text="Enter the Control's Function", blank=True)
    functionID = models.CharField(max_length=6, default='', help_text="Enter the Control's FunctionID", blank=True)
    category = models.CharField(max_length=300, default='', help_text="Enter the Control's Category", blank=True)
    categoryID = models.CharField(max_length=6, default='', help_text="Enter the Control's CategoryID", blank=True)
    category_statement = models.CharField(max_length=300, default='', help_text="Enter the Control's Category Statement", blank=True)
    subcategory = models.CharField(max_length=300, default='', help_text="Enter the Control's SubCategory", blank=True)
    subcategoryID = models.CharField(max_length=20, default='', help_text="Enter the Control's SubCategoryID", blank=True)
    control_statement = models.CharField(max_length=300, default='', help_text="Enter the Control Statement", blank=True)
    default_question = models.CharField(max_length=600, default='', help_text="Enter the Control's References", blank=True)
    reference = models.CharField(max_length=300, default='', help_text="Enter the Control's References", blank=True)

    evidencefile = models.FileField(upload_to='uploads', blank=True)
    #orderID = models.IntegerField(primary_key=True, null=False, editable=False, unique=True)
    #SourceID = models.ForeignKey(Source, , on_delete=models.CASCADE)
    objects = FrameworkControlsManager()
    # Metadata
    class Meta:
        ordering = ['order_id']

    def __str__(self):
        return self.function

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = FrameworkControls.objects.all().aggregate(largest=models.Max('order_id'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.order_id = last_id + 1

        super(FrameworkControls, self).save(*args, **kwargs)

# Create your models here.
class Assessment(models.Model):
    #orderID = models.IntegerField(primary_key=True, null=False, editable=False, unique=True)
    order_id = models.IntegerField(default=1)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this Assessment.', editable=False, unique=True)
    name = models.CharField(max_length=400, default='', help_text='Enter the Name of this Assessment', unique=True)
    vendor = models.ForeignKey(Company, related_name='+', on_delete=models.CASCADE)
    #VendorContact = models.ForeignKey(VendorPOC, on_delete=models.CASCADE)
    owner =  models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    vendor_contact = models.ForeignKey(User, on_delete=models.CASCADE)
    auditor = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, blank=True,null=True)
    analyst = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, blank=True,null=True)
    start_date = models.DateField(default=datetime.date.today)
    complete_date = models.DateField(blank=True, null=True)
    STATUS_CHOICES = [ ('CREATED', 'Created'),
        ('QUESTIONNAIRE_REVIEW', 'Questionnaire in Review'),
        ('VENDOR_SUBMIT', 'Submitted to Vendor'),
        ('IN_ANALYSIS', 'In Analysis'),
        ('REPORT_GENERATED', 'Report Generated'),
        ('ASSESSMENT_REVIEW', 'Assessment Under Review'),
        ('ASSESSMENT_COMPLETE', 'Assessment Complete'),]
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='CREATED')
    #Framework = models.ForeignKey(Framework, default='1', on_delete=models.CASCADE)
    frameworks = models.ManyToManyField('Framework', through='AssessmentFrameworks')

    #Frameworks = models.CharField(max_length=600, default='Frameworks...')
    #is_created                  = models.BooleanField(default=False, help_text="Has the Vendor Assessment been Created?", null=True)
    #is_questionnaire_reviewed   = models.BooleanField(default=False, help_text="Has the Vendor Assessment Questionnaire been Reviewed?", null=True)
    #is_submitted_to_vendor      = models.BooleanField(default=False, help_text="Has the Vendor Assessment been Submitted to the Vendor?", null=True)
    #is_submitted_for_analysis   = models.BooleanField(default=False, help_text="Has the Vendor Assessment Questionnaire been Submitted for Analyst?", null=True)
    #is_analysis_complete        = models.BooleanField(default=False, help_text="Has the Vendor Assessment Questionnaire been Anazlyzed?", null=True)
    #is_report_generated         = models.BooleanField(default=False, help_text="Has the Vendor Assessment Report been Generated?", null=True)
    #is_assessment_complete      = models.BooleanField(default=False, help_text="Has the Vendor Assessment Completed?", null=True)

    objects = AssessmentManager()
    # Metadata
    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = Assessment.objects.all().aggregate(largest=models.Max('order_id'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.order_id = last_id + 1
        super(Assessment, self).save(*args, **kwargs)


@receiver(post_save, sender=Assessment)

def create_Questionnaire(sender, instance=None, created=False, **kwargs):
    if created:
        Questionnaire.objects.create(assessment=instance)
        newQuestionnaire = Questionnaire.objects.last()
        q_uuid = newQuestionnaire.uuid
        newQuestionnaire.save()



class Questionnaire(models.Model):

    # fields
    #orderID = models.IntegerField(primary_key=True, null=False, editable=False, unique=True)
    order_id = models.IntegerField(default=1)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this Questionnaire.', editable=False, unique=True)
    assessment = models.ForeignKey(Assessment, related_name='+', on_delete=models.CASCADE)

    #objects = QuestionnaireManager()
    # Metadata
    class Meta:
        ordering = ['order_id']

    def __str__(self):
        return self.assessment

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = Questionnaire.objects.all().aggregate(largest=models.Max('order_id'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.order_id = last_id + 1
        super(Questionnaire, self).save(*args, **kwargs)
        #question_frameworks
        #Questionnaire.objects.create(assessment=instance)
        #newQuestionnaire = Questionnaire.objects.last()
        #q_uuid = newQuestionnaire.uuid
        #print(q_uuid)

def user_directory_path(instance, filename):
    # need to capture assesment uuid -- THAT'S the ROOT

    # file will be uploaded to MEDIA_ROOT/assessment_evidence/uuid-of-document/<filename>
    return '{0}/{1}/{2}'.format(instance.assessment.uuid, instance.uuid, filename)

class Document(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this Document.', editable=False, unique=True)
    #question = models.ForeignKey(Question, related_name='+', on_delete=models.CASCADE,blank=True,null=True)
    document = models.FileField(upload_to=user_directory_path)
    uploadDate = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=500, blank=True)
    description = models.CharField(max_length=500, blank=True)
    assessment = models.ForeignKey(Assessment, related_name='+', on_delete=models.CASCADE,blank=True,null=True)
    #question = models.ForeignKey(Question, related_name='+', on_delete=models.CASCADE,blank=True,null=True)

class Question(models.Model):
    ## question fields
    order_id = models.IntegerField(default=1)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this Question.', editable=False, unique=True)

    ## correllative fields
    questionnaire = models.ForeignKey(Questionnaire, related_name='+', on_delete=models.CASCADE,blank=True,null=True)
    assessment = models.ForeignKey(Assessment, related_name='+', on_delete=models.CASCADE,blank=True,null=True)
    control = models.ForeignKey(FrameworkControls, related_name='+', on_delete=models.CASCADE,blank=True,null=True)

    ## fields populated from the framework controls for each framework
    function = models.CharField(max_length=50, default='', help_text="The Control's Function",blank=True,null=True)
    functionID = models.CharField(max_length=6, default='', help_text="The Control's FunctionID",blank=True,null=True)
    category = models.CharField(max_length=300, default='', help_text="The Control's Category",blank=True,null=True)
    categoryID = models.CharField(max_length=6, default='', help_text="The Control's CategoryID",blank=True,null=True)
    category_statement = models.CharField(max_length=300, default='', help_text="The Control's Category Statement",blank=True,null=True)
    subcategory = models.CharField(max_length=300, default='', help_text="The Control's SubCategory",blank=True,null=True)
    subcategoryID = models.CharField(max_length=6, default='', help_text="The Control's SubCategoryID",blank=True,null=True)
    control_statement = models.CharField(max_length=300, default='', help_text="The Control Statement",blank=True,null=True)
    question = models.CharField(max_length=600, default='', help_text="Enter the assessment question.",blank=True,null=True)
    answer = models.CharField(max_length=600, default='', help_text="Enter the answer to assessment question.",blank=True,null=True)
    maturity = models.IntegerField(default='1', help_text="Enter the maturity level for the question.",blank=True,null=True)
    document = models.ForeignKey(Document, related_name='+', on_delete=models.CASCADE,blank=True,null=True)


    ## analysis fields
    compliance = models.BooleanField(default=True, help_text="Is the vendor's response and evidence compliant with your framework control?",blank=True,null=True)
    notes = models.CharField(max_length=400, default='', help_text='Enter any notes from the assessor.',blank=True,null=True)
    LIKELIHOOD_CHOICES = [ ('VERY_LOW', 'Very Low'), ('LOW', 'Low'), ('MODERATE', 'Moderate'), ('HIGH', 'High'), ('VERY_HIGH', 'Very High') ]
    likelihood = models.CharField(max_length=12, choices=LIKELIHOOD_CHOICES, default='MODERATE',blank=True,null=True)
    IMPACT_CHOICES = [ ('VERY_LOW', 'Very Low'), ('LOW', 'Low'), ('MODERATE', 'Moderate'), ('HIGH', 'High'), ('VERY_HIGH', 'Very High') ]
    impact = models.CharField(max_length=12, choices=IMPACT_CHOICES, default='MODERATE',blank=True,null=True)
    #SourceID = models.ForeignKey(Source, , on_delete=models.CASCADE)
    risk_rating = models.CharField(max_length=12, default='MODERATE',blank=True,null=True)
    was_analyzed = models.BooleanField(default=False, help_text="Did an analyst analyst this question?", blank=True, null=True)
    objects = QuestionManager()

    # Metadata
    class Meta:
        ordering = ['order_id']

    def __str__(self):
        return self.assessment

    def change_answer(self, new_answer):
        self.answer = new_answer
        self.save()
        return self.answer == new_answer

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = Question.objects.all().aggregate(largest=models.Max('order_id'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.order_id = last_id + 1
        super(Question, self).save(*args, **kwargs)

#class Document(models.Model):
#    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this Document.', editable=False, unique=True)
#    #question = models.ForeignKey(Question, related_name='+', on_delete=models.CASCADE,blank=True,null=True)
#    document = models.FileField(upload_to=user_directory_path)
#    uploadDate = models.DateTimeField(auto_now_add=True)
#    document_name = models.CharField(max_length=500, blank=True)
#    document_description = models.CharField(max_length=500, blank=True)
#    assessment = models.ForeignKey(Assessment, related_name='+', on_delete=models.CASCADE,blank=True,null=True)
#    question = models.ForeignKey(Question, related_name='+', on_delete=models.CASCADE,blank=True,null=True)

class AssessmentFrameworks(models.Model):
    framework = models.ForeignKey(Framework, related_name='+', on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, related_name='+', on_delete=models.CASCADE)

class Report(models.Model):
    def framework_based_upload_to(instance, filename):
        return "uploads/{}/{}".format(instance.uuid, filename)


    order_id = models.IntegerField(default=1)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this Report.', editable=False, unique=True)
    name = models.CharField(max_length=200, default='Report', blank=True, unique=True)
    questionnaire = models.ForeignKey(Questionnaire, related_name='+', on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, related_name='+', on_delete=models.CASCADE)
    executive_summary = models.CharField(max_length=6000, default='', help_text='Write in your executive summary here.',blank=True,null=True)
    executive_findings = models.CharField(max_length=2000, default='', help_text='Write in your executive findings here.',blank=True,null=True)
    executive_compliance_summary = models.CharField(max_length=6000, default='', help_text='Write in your executive findings summary here.',blank=True,null=True)
    executive_risk_assessment_summary = models.CharField(max_length=6000, default='', help_text='Write in your executive risk assessment summary here.',blank=True,null=True)
    #executive_compliance_chart = models.FileField(upload_to=framework_based_upload_to, blank=True)
    #executive_risk_chart = models.FileField(upload_to=framework_based_upload_to, blank=True)

    executive_compliance_chart = models.ImageField(upload_to=framework_based_upload_to, blank=True)
    executive_risk_chart = models.ImageField(upload_to=framework_based_upload_to, blank=True)


    #executive_compliance_chart = models.CharField(max_length=6000, default='', help_text='',blank=True,null=True)
    #executive_risk_chart = models.CharField(max_length=6000, default='', help_text='',blank=True,null=True)
    nc_controls = models.IntegerField(null=True, blank=True)
    c_controls = models.IntegerField(null=True, blank=True)
    author = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE,blank=True,null=True)
    publication_date = models.DateField(default=datetime.date.today, help_text="Enter the date the report was published",blank=True,null=True)

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = Report.objects.all().aggregate(largest=models.Max('order_id'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.order_id = last_id + 1
        super(Report, self).save(*args, **kwargs)
