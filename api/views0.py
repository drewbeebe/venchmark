# api/views.py
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from assessments.models import Assessment, Framework, FrameworkSource, FrameworkControls, Questionnaire, Question, Report
from companies.models import Company, User
#from frameworks import models as frameworkmodels
#from companies import models as companiesmodels
from . import serializers
from rest_framework import authentication, permissions
from django.db.models.fields import CharField
from . import cipher

# EncryptedField
class EnField(CharField):
    #def from_db_value(self, value, expression, connection):
    def from_db_value(self, value):
        """ Decrypt the data for display in Django as normal. """
        return cipher.decrypt(value)
    def get_prep_value(self, value):
        """ Encrypt the data when saving it into the database. """
        return cipher.encrypt(value)

    #EnField(max_length=12, choices=RISK_RATING_CHOICES, default='MODERATE')


class ListQuestions(generics.ListCreateAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = serializers.QuestionnaireSerializer


class DetailQuestions(generics.RetrieveUpdateDestroyAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = serializers.QuestionnaireSerializer

class ListAssessments(generics.ListCreateAPIView):

    queryset = Assessment.objects.all().filter()
    serializer_class = serializers.AssessmentsSerializer

class DetailAssessments(generics.RetrieveUpdateDestroyAPIView):
    queryset = Questionnaire.objects.all().filter()
    serializer_class = serializers.AssessmentsSerializer

class RetrieveControls(generics.ListCreateAPIView):
#class RetrieveControls(APIView):
    #permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    #group_required = [ u"administrator" ]
    #queryset = models.FrameworkControls.objects.all().filter(FrameworkID=self.kwargs['framework_id'])
    serializer_class = serializers.ControlsSerializer
    #slug_url_kwarg = FrameworkControls.frameworkUUID

    def get_queryset(self):
         #if self.kwargs['FrameworkID_id']:
         #passed_uuid = str(self.kwargs['uuid'])
         if self.kwargs['uuid']:
         #if self.kwargs['uuid']:
             #print(str(self.kwargs['uuid']))
             #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid']).order_by('id')  #.order_by('orderID')
             #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid'])  #.order_by('orderID')
             return FrameworkControls.objects.filter(frameworkID=self.kwargs['uuid']).order_by('order_id')  #.order_by('orderID')
         else:
             return FrameworkControls.objects.all()  #.order_by('orderID')
    #def get(self, request, uuid):
        #print("passed kwarg = " + str(slug_url_kwarg))
        #print("passed kwarg = " + str(self.kwargs['uuid']))

    #    """
    #    Return a list of all users.
    #    """
    ##    return Response(controls)

class RetrieveSingleControl(generics.ListCreateAPIView):
#class RetrieveControls(APIView):
    #permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    #group_required = [ u"administrator" ]
    #queryset = models.FrameworkControls.objects.all().filter(FrameworkID=self.kwargs['framework_id'])
    serializer_class = serializers.ControlsSerializer
    #slug_url_kwarg = FrameworkControls.frameworkUUID

    def get_queryset(self):
         #if self.kwargs['FrameworkID_id']:
         #passed_uuid = str(self.kwargs['uuid'])
         if self.kwargs['uuid']:
         #if self.kwargs['uuid']:
             #print(str(self.kwargs['uuid']))
             #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid']).order_by('id')  #.order_by('orderID')
             #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid'])  #.order_by('orderID')
             return FrameworkControls.objects.filter(uuid=self.kwargs['uuid']).order_by('order_id')  #.order_by('orderID')
         else:
             return FrameworkControls.objects.all()  #.order_by('orderID')

class RetrieveControlsByFramework(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ControlsSerializerv2

    def get_queryset(self):
         associated_fw = Framework.objects.filter(id=self.kwargs['id'])
         fw = associated_fw.first()
         fw_order_uuid = fw.uuid

         #if self.kwargs['id']:
         if fw_order_id:
             return FrameworkControls.objects.filter(frameworkID_id=fw_order_uuid).order_by('id')
         else:
             return FrameworkControls.objects.all().first()  #.order_by('orderID')
             #return models.FrameworkControls.objects.none()  #.order_by('orderID')

class ListFrameworks(generics.ListCreateAPIView):
    queryset = Framework.objects.all().filter()
    serializer_class = serializers.FrameworkSerializer

class DetailFrameworks(generics.RetrieveUpdateDestroyAPIView):
    queryset = Framework.objects.all()
    serializer_class = serializers.FrameworkSerializer

#class ListControls(generics.ListCreateAPIView):
#    #queryset = models.Framework.objects.all().filter()
#    serializer_class = serializers.FrameworkSerializer
#    slug_url_kwarg = FrameworkControls.uuid
#    fields = '__all__'
#    def get_object(self, queryset=None):
#        obj = FrameworkFrameworkControls.objects.filter(id=self.kwargs['id']).first()
#        return obj
#    def get_queryset(self):
#        print("self kwarg id:" + self.kwargs['id'])
#        queryset = FrameworkControls.objects.filter(id=self.kwargs['id']).first()
#        return queryset

class RetrieveCompaniesAPIView(generics.ListCreateAPIView):
#class RetrieveControls(APIView):
    #permission_classes = [IsAuthenticated]

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    #group_required = [ u"administrator" ]
    #queryset = models.FrameworkControls.objects.all().filter(FrameworkID=self.kwargs['framework_id'])
    serializer_class = serializers.CompanySerializer
    #queryset = Company.objects.filter(uuid='pk')


    def get_queryset(self):
        #print("Here's an arg: " + str(self.kwargs))

        if self.kwargs['id']:
        #if self.kwargs['uuid']:
            #print(str(self.kwargs['uuid']))
            #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid']).order_by('id')  #.order_by('orderID')
            #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid'])  #.order_by('orderID')
            return Company.objects.filter(uuid=self.kwargs['id']).order_by('order_id')  #.order_by('orderID')
        else:
            print("returning all companies ... ")
            return Company.objects.all().order_by('order_id')  #.order_by('orderID')



class RetrieveAllCompaniesAPIView(generics.ListCreateAPIView):
#class RetrieveControls(APIView):
    #permission_classes = [IsAuthenticated]

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    #group_required = [ u"administrator" ]
    #queryset = models.FrameworkControls.objects.all().filter(FrameworkID=self.kwargs['framework_id'])
    serializer_class = serializers.CompanySerializer
    queryset = Company.objects.all().order_by('order_id')

class RetrieveAllUsersAPIView(generics.ListCreateAPIView):
#class RetrieveControls(APIView):
    #permission_classes = [IsAuthenticated]

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    #group_required = [ u"administrator" ]
    #queryset = models.FrameworkControls.objects.all().filter(FrameworkID=self.kwargs['framework_id'])
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

class RetrieveUserAPIView(generics.ListCreateAPIView):
#class RetrieveControls(APIView):
    #permission_classes = [IsAuthenticated]

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    #group_required = [ u"administrator" ]
    #queryset = models.FrameworkControls.objects.all().filter(FrameworkID=self.kwargs['framework_id'])
    serializer_class = serializers.UserSerializer
    #queryset = User.objects.all()
    def get_queryset(self):
        #print("Here's an arg: " + str(self.kwargs))

        if self.kwargs['uuid']:
        #if self.kwargs['uuid']:
            #print(str(self.kwargs['uuid']))
            #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid']).order_by('id')  #.order_by('orderID')
            #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid'])  #.order_by('orderID')
            #return User.objects.filter(uuid=self.kwargs['uuid']).order_by('id')  #.order_by('orderID')
            return User.objects.filter(uuid=self.kwargs['uuid'])  #.order_by('orderID')
        else:
            return User.objects.all()  #.order_by('orderID')


class RetrieveAllFrameworksAPIView(generics.ListCreateAPIView):
#class RetrieveControls(APIView):
    #permission_classes = [IsAuthenticated]

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    #group_required = [ u"administrator" ]
    #queryset = models.FrameworkControls.objects.all().filter(FrameworkID=self.kwargs['framework_id'])
    serializer_class = serializers.FrameworkSerializer
    queryset = Framework.objects.all()

class RetrieveQuestionsbyAssessmentAPIView(generics.ListCreateAPIView):
#class RetrieveControls(APIView):
    #permission_classes = [IsAuthenticated]

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    #group_required = [ u"administrator" ]
    #queryset = models.FrameworkControls.objects.all().filter(FrameworkID=self.kwargs['framework_id'])
    serializer_class = serializers.QuestionSerializer
    #queryset = User.objects.all()
    def get_queryset(self):
        #print("Here's an arg: " + str(self.kwargs))

        if self.kwargs['uuid']:
        #if self.kwargs['uuid']:
            #print(str(self.kwargs['uuid']))
            #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid']).order_by('id')  #.order_by('orderID')
            #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid'])  #.order_by('orderID')
            #return User.objects.filter(uuid=self.kwargs['uuid']).order_by('id')  #.order_by('orderID')
            return Question.objects.filter(assessment_id=self.kwargs['uuid'])  #.order_by('orderID')
        #else:
            #return Question.objects.all()  #.order_by('orderID')

class AssessmentDetailsAPIVIew(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    #queryset = Questionnaire.objects.all().filter()
    serializer_class = serializers.AssessmentsSerializer

    def get_queryset(self):
        #print("Here's an arg: " + str(self.kwargs))

        if self.kwargs['uuid']:
        #if self.kwargs['uuid']:
            #print(str(self.kwargs['uuid']))
            #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid']).order_by('id')  #.order_by('orderID')
            #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid'])  #.order_by('orderID')
            #return User.objects.filter(uuid=self.kwargs['uuid']).order_by('id')  #.order_by('orderID')
            return Assessment.objects.filter(uuid=self.kwargs['uuid'])  #.order_by('orderID')
        #else:

class RetrieveCompaniesRiskAPIView(APIView):
#class StatsCompaniesSerializer(APIView):
        def get(self, request, format=None):
            high_vendors = 0
            moderate_vendors = 0
            low_vendors = 0

            companies = Company.objects.all()
            for company in companies:
                # decrypt risk_rating
                risk_rating = company.risk_rating
                #print(risk_rating)
                #risk_rating = EnField(max_length=12, choices=RISK_RATING_CHOICES, default='MODERATE')
                #dec_rr = cipher.decrypt(risk_rating)
                #enc_rr = EnField.from_db_value(self, risk_rating)
                #print(risk_rating)
                #rr = str(risk_rating)
                #print(rr)
                # read risk_rating and
                if risk_rating == "HIGH":
                    high_vendors += 1;
                elif risk_rating == "MODERATE":
                    moderate_vendors += 1;
                elif risk_rating == "LOW":
                    low_vendors += 1;
                # select case for
                # if high, add counter to high count
                # if moderate, add counter to moderate count
                # if low, add counter to low count
            data = {
                "labels": ["High Risk Vendors", "Moderate Risk Vendors", "Low Risk Vendors"],
                "high_vendors": [high_vendors],
                "moderate_vendors": [moderate_vendors],
                "low_vendors": [low_vendors],

            }
            default_items = ["labels", "high_vendors", "moderate_vendors", "low_vendors"]
            return Response(data)

class RetrieveCompaniesDataAPIView(APIView):
#class StatsCompaniesSerializer(APIView):
        def get(self, request, format=None):
            high_vendors = 0
            moderate_vendors = 0
            low_vendors = 0

            companies = Company.objects.all()
            for company in companies:
                # decrypt risk_rating
                data_rating = company.data_sensitivity_rating
                #print(risk_rating)
                #risk_rating = EnField(max_length=12, choices=RISK_RATING_CHOICES, default='MODERATE')
                #dec_rr = cipher.decrypt(risk_rating)
                #enc_rr = EnField.from_db_value(self, risk_rating)
                #print(risk_rating)
                #rr = str(risk_rating)
                #print(rr)
                # read risk_rating and
                if data_rating == "HIGH":
                    high_vendors += 1;
                elif data_rating == "MODERATE":
                    moderate_vendors += 1;
                elif data_rating == "LOW":
                    low_vendors += 1;
                # select case for
                # if high, add counter to high count
                # if moderate, add counter to moderate count
                # if low, add counter to low count
            data = {
                "labels": ["Vendors /w High Risk Data", "Vendors w/ Moderate Risk Data", "Vendors w/ Low Risk Data"],
                "high_vendors": [high_vendors],
                "moderate_vendors": [moderate_vendors],
                "low_vendors": [low_vendors],

            }
            default_items = ["labels", "high_vendors", "moderate_vendors", "low_vendors"]
            return Response(data)


class ReportDetailAPIVIew(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    #queryset = Questionnaire.objects.all().filter()
    serializer_class = serializers.ReportsSerializer

    def get_queryset(self):
        #print("Here's an arg: " + str(self.kwargs))

        if self.kwargs['uuid']:
        #if self.kwargs['uuid']:
            #print(str(self.kwargs['uuid']))
            #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid']).order_by('id')  #.order_by('orderID')
            #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid'])  #.order_by('orderID')
            #return User.objects.filter(uuid=self.kwargs['uuid']).order_by('id')  #.order_by('orderID')
            return Reports.objects.filter(uuid=self.kwargs['uuid'])  #.order_by('orderID')
        #else:

class ReportsListAPIVIew(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    #queryset = Questionnaire.objects.all().filter()
    serializer_class = serializers.ReportsSerializer
    queryset = Report.objects.all()
    #def get_queryset(self):
    #    #print("Here's an arg: " + str(self.kwargs))

    #    if self.kwargs['uuid']:
        #if self.kwargs['uuid']:
            #print(str(self.kwargs['uuid']))
            #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid']).order_by('id')  #.order_by('orderID')
            #return FrameworkControls.objects.filter(frameworkUUID=self.kwargs['uuid'])  #.order_by('orderID')
            #return User.objects.filter(uuid=self.kwargs['uuid']).order_by('id')  #.order_by('orderID')
    #        return Reports.objects.filter(uuid=self.kwargs['uuid'])  #.order_by('orderID')
        #else:

class RetrieveSingleCompanyComplianceAPIView(APIView):
        #uuid = self.kwargs['uuid']
        #return Reports.objects.filter(uuid=self.kwargs['uuid'])
        #def get_queryset(self):
        #    if self.kwargs['uuid']:
        #    print(self.kwargs['uuid'])
        #    return questions = Question.objects.filter(assessment_id=self.kwargs['uuid'])

        def get(self, request, uuid, format=None):
            #uuid = request.kwargs['uuid']
            compliant_controls = 0
            non_compliant_controls = 0
            #partially-compliant_controls = 0
            #uuid = self.kwargs['uuid']
            questions = Question.objects.filter(assessment_id=uuid)


            for question in questions:
                if question.compliance == "True":
                    compliant_controls += 1;
                elif question.compliance == "False":
                    non_compliant_controls += 1;

                #need to turn 'compliance' this binary field into a charfield to allow for partially_compliant
                #elif risk_rating == "LOW":
                #    low_vendors += 1;
                # select case for
                # if high, add counter to high count
                # if moderate, add counter to moderate count
                # if low, add counter to low count
            data = {
                "labels": ["Compliant Controls", "Non-Compliant Controls" ],
                "compliant_controls": [compliant_controls],
                "non-compliant_controls": [non_compliant_controls],
            }
            default_items = ["labels", "compliant_controls", "non_compliant_controls" ]
            return Response(data)


class RetrieveSingleCompanyRiskAPIView(APIView):

        def get(self, request, uuid, format=None):
            #uuid = request.kwargs['uuid']
            high_risk_controls = 0
            moderate_risk_controls = 0
            low_risk_controls = 0

            questions = Question.objects.filter(assessment_id=uuid)


            for question in questions:
                if question.risk_rating == "HIGH":
                    high_risk_controls += 1;
                elif question.risk_rating == "MODERATE":
                    moderate_risk_controls += 1;
                elif question.risk_rating == "LOW":
                    low_risk_controls += 1;


            data = {
                "labels": ["High Risk Controls", "Moderate Risk Controls", "Low Risk Controls" ],
                "high_risk_controls": [high_risk_controls],
                "moderate_risk_controls": [moderate_risk_controls],
                "low_risk_controls": [low_risk_controls],
            }
            default_items = ["labels", "high_risk_controls", "moderate_risk_controls", "low_risk_controls"]
            return Response(data)
