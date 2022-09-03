import os
import csv

from . models import Framework, FrameworkSource, FrameworkControls, Assessment, Questionnaire, AssessmentFrameworks, Question
from django.conf import settings
from django.conf.urls.static import static

def CloneFramework(uuid):
    print("cloning ... ")
    framework_to_clone = Framework.objects.filter(uuid=uuid).first()
    print(framework_to_clone.name)
    NewFramework = Framework()
    NewFramework.name = framework_to_clone.name + " - clone"
    NewFramework.short_name = framework_to_clone.short_name
    NewFramework.version = framework_to_clone.version
    NewFramework.publication_date = framework_to_clone.publication_date
    NewFramework.source = framework_to_clone.source
    NewFramework.save()
    LatestFramework = Framework.objects.latest('order_id')
    LFUUID = LatestFramework.uuid
    print("UUID to assign to cloned controls ... [for new framework]: " + str(LFUUID))

    CloneFrameworkControls = FrameworkControls.objects.filter(framework.uuid==uuid)

    for control in CloneFrameworkControls:
        print("cloning " + control.subcategoryID)
        NewControl = FrameworkControls()
        NewControl.framework = control.framework
        NewControl.frameworkUUID = LFUUID
        NewControl.function = control.function
        NewControl.functionID = control.functionID
        NewControl.category = control.category
        NewControl.categoryID = control.categoryID
        NewControl.category_statement = control.category_statement
        NewControl.subcategory = control.subcategory
        NewControl.subcategoryID = control.subcategoryID
        #NewControl.control_statement = control.control_statement
        NewControl.default_question = control.default_question
        NewControl.reference = control.reference
        NewControl.save()

def handle_uploaded_file(f, uuid):

    framework_to_add_controls = Framework.objects.filter(uuid=uuid).first()
    print("framework for control addition: " + str(framework_to_add_controls.uuid))

    #define framework upload directory
    framework_file_save_dir = "uploads/{}".format(uuid)
    upload_path = os.path.join(settings.BASE_DIR, framework_file_save_dir)


    ## make framework-uuid named directory if it doesn't exist
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    #controls_file_save_name = "uploads/{}/{}".format(uuid, filename)

    filename = str(f)
    #upload_file_to = os.path.join(settings.BASE_DIR, controls_file_save_name)
    upload_file_to = os.path.join(upload_path, filename)
    #print(filename)
    #print(controls_file_save_name)
    with open(upload_file_to, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    destination.close()

    with open(upload_file_to, newline='') as csvfile:
        control_reader = csv.DictReader(csvfile, delimiter=',')
        line_count = 0
        for row in control_reader:
            NewControl = FrameworkControls()
            if line_count == 0:
                #print(row['function'] + "," + row['functionID'] + "," + row['category'] + "," + row['categoryID'] + "," + row['category_statement'])
                print("Header Row")
                print(row['function'] + "," + row['functionID'] + "," + row['category'] + "," + row['categoryID'] + "," + row['category_statement'])
                print("printing raw row")
                print(row)
                line_count += 1
            print(row['function'] + "," + row['functionID'] + "," + row['category'] + "," + row['categoryID'] + "," + row['category_statement'])
            NewControl.frameworkUUID = str(uuid)
            NewControl.framework_id = str(uuid)
            NewControl.framework = framework_to_add_controls
            NewControl.function = row['function']
            NewControl.functionID = row['functionID']
            NewControl.category = row['category']
            NewControl.categoryID = row['categoryID']
            NewControl.category_statement = row['category_statement']
            NewControl.subcategory = row['subcategory']
            NewControl.subcategoryID = row['subcategoryID']
            NewControl.default_question = row['default_question']
            NewControl.reference = row['reference']
            NewControl.save()
            line_count += 1
        #print(f'Processed {line_count} lines.')

def PopulateQuestions(assessment_uuid, questionnaire_uuid):
    print("Assessment ID: " + str(assessment_uuid))
    print("Questionnaire ID: " + str(questionnaire_uuid))
    questionnaire = Questionnaire.objects.filter(uuid=questionnaire_uuid).first()
    assessment    = Assessment.objects.get(uuid=assessment_uuid)
    aframework_set = assessment.frameworks.all()
    #aframework_set = AssessmentFrameworks.objects.filter(assessment=assessment_uuid)

    for afwork in aframework_set:
        #print("Processing framework:" + str(afwork.framework.name))
        print("Processing framework: " + str(afwork))
        controls_set = FrameworkControls.objects.filter(frameworkUUID=afwork.uuid)
        print("Number of controls to create questions from: " + str(controls_set.count()))
        for ctrl in controls_set:
            print("Processing control: " + ctrl.categoryID)
            NewQuestion = Question()
            NewQuestion.questionnaire = questionnaire
            NewQuestion.assessment = questionnaire.assessment
            NewQuestion.control = ctrl
            NewQuestion.question = ctrl.default_question
            NewQuestion.save()
