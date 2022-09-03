
from django import template
from .. models import Assessment, Questionnaire, Question

register = template.Library()

@register.filter(name='pct_complete')
def pct_complete(uuid):
    thisassessment = Assessment.objects.filter(uuid=uuid)
    questions_list = Question.objects.filter(assessment=uuid)
    total_num_questions = questions_list.count()
    num_questions_answer = 0
    pct_complete = 0

    for question in questions_list:
        if question.answer != "":
            num_questions_answer += 1

    pct_complete = num_questions_answer / total_num_questions
    return int(pct_complete)


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
