# financial controls

from django.db import migrations
from .. import financial_controls as financialcontrols
from .. models import Framework, FrameworkSource, FrameworkControls
import uuid

def load_frameworksources(apps, schema_editor):
    #NewFrameworkSource = apps.get_model("frameworks", "FrameworkSource")
    NewFrameworkSource = FrameworkSource()
    NewFrameworkSource.uuid =  str("f3997d33bbdb42b8afad4818ecaf9106")  #uuid.uuid4()#uuid.UUIDField("39dd004ac1a940f8a86eada854d6332e")
    NewFrameworkSource.name = "Venchmark"
    NewFrameworkSource.acronym = "VMARK"
    NewFrameworkSource.url = "https://www.venchmark.com"
    NewFrameworkSource.save()

    #NewFrameworkSource = FrameworkSource()
    #NewFrameworkSource.id = str("45e74db0651441d8bcd424ef17ec5fb1")  #uuid.uuid4()#uuid.UUIDField("45e74db0651441d8bcd424ef17ec5fb1")
    #NewFrameworkSource.Name = "International Organization for Standardization"
    #NewFrameworkSource.Acronym = "ISO"
    #NewFrameworkSource.URL = "https://www.iso.org/home.html"
    #NewFrameworkSource.save()
    #National Institute for Standards and Technology|NIST|https://www.nist.gov|39dd004ac1a940f8a86eada854d6332e
    #International Organization for Standardization|ISO|https://www.iso.org/home.html|45e74db0651441d8bcd424ef17ec5fb1

    #id | Name | Acronym | URL

def load_frameworks(apps, schema_editor):
    #NewFramework = apps.get_model('frameworks', 'Framework')
    NewFramework = Framework()
    NewFramework.uuid = uuid.uuid4() #"55f27b8d74af48dfaee7389bb1d76c20"
    NewFramework.name = "Financial Framework for Reviewing Vendor Viability"
    NewFramework.short_name = "FIN"
    NewFramework.version = "1.0"
    NewFramework.publish_date = "2021-01-01"
    #newsource = FrameworkSource.objects.
    newsource = FrameworkSource.objects.filter(uuid="f3997d33bbdb42b8afad4818ecaf9106").first()
    #print(str(query.id))
    NewFramework.source = newsource #"39dd004ac1a940f8a86eada854d6332e"
    NewFramework.save()

def load_controls(apps, schema_editor):
    NewFrameworkControl = apps.get_model('assessments', 'FrameworkControls')

    financial_controls = []
    financial_controls = financialcontrols.financial_default_controls_and_questions

    for control in financial_controls:
        #framework = control[0]
        function = control[0]
        functionID = control[1]
        category = control[2]
        categoryID = control[3]
        category_statement = control[4]
        subcategoryID = control[5]
        control_statement = control[6]
        default_question = control[7]
        NewFrameworkControl = FrameworkControls()
        NewFrameworkControl.uuid = uuid.uuid4() #"39dd004ac1a940f8a86eada854d6332e"
        query = Framework.objects.first()
        NewFrameworkControl.framework = query #framework
        NewFrameworkControl.frameworkUUID = query.uuid #FrameworkUUID
        NewFrameworkControl.function = functionID
        NewFrameworkControl.category = category
        NewFrameworkControl.categoryID = categoryID
        NewFrameworkControl.category_statement = category_statement
        #NewFrameworkControl.SubCategory = subcategory
        NewFrameworkControl.subcategoryID = subcategoryID
        NewFrameworkControl.control_statement = control_statement
        NewFrameworkControl.default_question = default_question
        NewFrameworkControl.save()


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0004_nist_800171'),
    ]

    operations = [
        migrations.RunPython(load_frameworksources),
        migrations.RunPython(load_frameworks),
        migrations.RunPython(load_controls),
    ]
