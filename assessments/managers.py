from django.utils.translation import gettext_lazy as _
from django.db import models

from django.db.models import Q # new
from itertools import chain



class FrameworkSourceManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(name__icontains=query) |
                         Q(acronym__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class FrameworkManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(name__icontains=query) |
                         Q(short_name__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class FrameworkControlsManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(function=query) |
                         Q(category__icontains=query) |
                         Q(categoryID__icontains=query) |
                         Q(category_statement__icontains=query) |
                         Q(subcategoryID__icontains=query) |
                         Q(control_statement__icontains=query) |
                         Q(default_question__icontains=query) |
                         Q(reference__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class AssessmentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(name__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


#class QuestionnaireManager(models.Manager):
    #def search(self, query=None):
    #    qs = self.get_queryset()
    #    if query is not None:
    #        or_lookup = (Q(assessment__icontains=query) |
    #                     Q(question__icontains=query)|
    #                     Q(answer__icontains=query)
    #                    )
    #        qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
    #    return qs


class QuestionManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(questionnaire__icontains=query) |
                         Q(question__icontains=query)|
                         Q(answer__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs
