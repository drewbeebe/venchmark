from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from assessments.models import Assessment, Framework, FrameworkSource, FrameworkControls
from companies.models import Company, User
#from frameworks.models import Framework, FrameworkSource, FrameworkControls
from itertools import chain

# Create your views here.
class SearchResultsView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"owner", u"administrator"]

    login_url = '/'
    template_name = 'search_results.html'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            company_results                 = Company.objects.search(query)
            user_results                    = User.objects.search(query)
            framework_results               = Framework.objects.search(query)
            frameworksource_results         = FrameworkSource.objects.search(query)
            frameworkcontrols_results       = FrameworkControls.objects.search(query)
            assessments_results             = Assessment.objects.search(query)

            # combine querysets
            queryset_chain = chain(
                    company_results,
                    user_results,
                    framework_results,
                    frameworksource_results,
                    frameworkcontrols_results,
                    assessments_results,
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=False)
            self.count = len(qs) # since qs is actually a list
            return qs
        return Framework.objects.none() # just an empty queryset as default
