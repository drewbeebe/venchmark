# Generated by Django 3.0.2 on 2021-02-05 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0001_initial'),
        ('assessments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='report',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='assessments.Questionnaire'),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='assessment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='assessments.Assessment'),
        ),
        migrations.AddField(
            model_name='question',
            name='assessment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='assessments.Assessment'),
        ),
        migrations.AddField(
            model_name='question',
            name='control',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='assessments.FrameworkControls'),
        ),
        migrations.AddField(
            model_name='question',
            name='document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='assessments.Document'),
        ),
        migrations.AddField(
            model_name='question',
            name='questionnaire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='assessments.Questionnaire'),
        ),
        migrations.AddField(
            model_name='frameworkcontrols',
            name='framework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='assessments.Framework'),
        ),
        migrations.AddField(
            model_name='framework',
            name='assessments',
            field=models.ManyToManyField(through='assessments.AssessmentFrameworks', to='assessments.Assessment'),
        ),
        migrations.AddField(
            model_name='framework',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='assessments.FrameworkSource'),
        ),
        migrations.AddField(
            model_name='document',
            name='assessment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='assessments.Assessment'),
        ),
        migrations.AddField(
            model_name='assessmentframeworks',
            name='assessment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='assessments.Assessment'),
        ),
        migrations.AddField(
            model_name='assessmentframeworks',
            name='framework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='assessments.Framework'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='analyst',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assessment',
            name='auditor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assessment',
            name='frameworks',
            field=models.ManyToManyField(through='assessments.AssessmentFrameworks', to='assessments.Framework'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assessment',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='companies.Company'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='vendor_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
