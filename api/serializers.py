# api/serializers.py
from rest_framework import serializers
from assessments.models import Framework, FrameworkSource, FrameworkControls, Assessment, Questionnaire, Question, Report
from companies.models import Company, User

class UserSerializer(serializers.ModelSerializer):
    #order_id = serializers.IntegerField(read_only=True)
    #username = serializers.StringRelatedField(read_only=True)
    #first_name = serializers.CharField(read_only=True)
    #last_name = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = (
            #'order_id',
            'uuid',
            'email',
            #'username',
            'first_name',
            'last_name',
            #'email',
            #'phone',
            #'vendor',
            #'department',
            'is_superuser',
        )

class FrameworkSourceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            #'order_id',
            'uuid',
            'name',
            'acronym',
            'url',
            )
        model = FrameworkSource

class FrameworkSerializer(serializers.ModelSerializer):
    #source = FrameworkSourceSerializer(many=False, read_only=False)
    class Meta:
        fields = (
            'uuid',
            'name',
            'short_name',
            'version',
            'publish_date',
            #'uuid',
            #'source',
        )
        model = Framework

class ControlsSerializer(serializers.ModelSerializer):
    #framework = FrameworkSerializer(many=False, read_only=False)
    class Meta:
        fields = (
            'order_id',
            'uuid',
            'frameworkID',
            'frameworkUUID',
            'function',
            'functionID',
            'category',
            'categoryID',
            'category_statement',
            'subcategory',
            'subcategoryID',
            'control_statement',
            'default_question',
            'reference'
        )
        model = FrameworkControls

class ControlsSerializerv2(serializers.ModelSerializer):
    framework = FrameworkSerializer(many=False, read_only=False)
    class Meta:
        fields = (
            #'url',
            'framework',
            'frameworkUUID',
            'function',
            'functionID',
            'category',
            'categoryID',
            'category_statement',
            'subcategory',
            'subcategoryID',
            'control_statement',
            'default_question',
            'reference'
        )
        model = FrameworkControls
        #lookup_field = 'FrameworkID'
        #extra_kwargs = {
    #        'url': {'lookup_field': 'FrameworkID'}
    #    }



class CompanySerializer(serializers.ModelSerializer):
    relationship_owner = UserSerializer(many=False, read_only=False)
    #ro = relationship_owner.objects.first()
    #ro_username = ro.username
    #owner_name = str(ro.last_name) + ", " + str(ro.first_name)
    class Meta:
        model = Company
        fields = (
            'order_id',
            'uuid',
            'name',
            'address1',
            'address2',
            'city',
            'state',
            'zip',
            'country',
            'url',
            'enrolled_date',
            'relationship_owner',
            'data_sensitivity_rating',
            'risk_rating',
        )
        model = Company

class AssessmentsSerializer(serializers.ModelSerializer):
#    vendor = CompanySerializer(many=False, read_only=False)
#    owner = UserSerializer(many=False, read_only=False)
#    vendor_contact = UserSerializer(many=False, read_only=False)
#    auditor = UserSerializer(many=False, read_only=False)
#    analyst = UserSerializer(many=False, read_only=False)
#    frameworks = FrameworkSerializer(many=True, read_only=False)

    #owner_name = owner.first_name + " " + owner.last_name
    #vendor_name = vendor.name
    #vencontact_name = vendor_contact.first_name + " " + vendor_contact.last_name
    #auditor_name = auditor.first_name + " " + auditor.last_name
    #analyst_name = analyst.first_name + " " + analyst.last_name

    class Meta:
        fields = (
            'order_id',
            'uuid',
            'name',
            'start_date',
            'complete_date',
            'status',
#            'frameworks',
        )
        model = Assessment


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'uuid',
            'assessment',
        )
        model = Questionnaire

class QuestionSerializer(serializers.ModelSerializer):
    questionnaire = QuestionnaireSerializer(many=False, read_only=False)
    assessment = AssessmentsSerializer(many=False, read_only=False)
    control = ControlsSerializer(many=False, read_only=False)
    class Meta:
        fields = (
            'order_id',
            'uuid',
            'questionnaire',
            'assessment',
            'control',
            'question',
            'answer',
            'compliance',
            'notes',
            'likelihood',
            'impact',
            'risk_rating',
        )
        model = Question

class AnalysisSerializer(serializers.ModelSerializer):
    questionnaire = QuestionnaireSerializer(many=False, read_only=False)
    assessment = AssessmentsSerializer(many=False, read_only=False)
    control = ControlsSerializer(many=False, read_only=False)
    class Meta:
        fields = (
            'order_id',
            'uuid',
            'questionnaire',
            'assessment',
            'control',
            'question',
            'answer',
            'compliance',
            'notes',
            'likelihood',
            'impact',
            'risk_rating',
        )
        model = Question

class ReportsSerializer(serializers.ModelSerializer):
    questionnaire = QuestionnaireSerializer(many=False, read_only=False)
    assessment = AssessmentsSerializer(many=False, read_only=False)
    author = UserSerializer(many=False, read_only=False)
    #control = ControlsSerializer(many=False, read_only=False)
    class Meta:
        fields = (
            'order_id',
            'uuid',
            'name',
            'questionnaire',
            'assessment',
            'executive_summary',
            'executive_compliance_summary',
            'executive_risk_assessment_summary',
            'c_controls',
            'nc_controls',
            'author',
            'publish_date'
        )
        model = Report
