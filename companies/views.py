from __future__ import print_function
from __future__ import unicode_literals
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Company, User
from .forms import CompanyListForm, CompanyDetailForm, CompanyModifyForm, CrispyCompanyForm, NewCompanyForm, UserAdminCreationForm, UserAdminChangeForm, RegisterForm, RegisterForm2, NewPersonForm, UpdatePersonForm, UpdateCompanyForm

from django.conf import settings
from django.core.mail import send_mail

from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView, FormView
from braces.views import GroupRequiredMixin
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from dal import autocomplete
#from django.contrib.auth
#from people.models import Person

# people/views.py
#from .admin import PersonProfileForm



class CompanyListView(GroupRequiredMixin, ListView):
    group_required = [u"owner", u"auditor", u"administrator"]

    login_url = '/'
    #raise_exception = True
    #redirect_field_name = REDIRECT_FIELD_NAME
    redirect_unauthenticated_users = True
    model = Company
    context_object_name = 'company_list'   # your own name for the list as a template variable
    queryset = Company.objects.filter(is_vendor=True)
    fields = [ 'name', 'address1', 'address2', 'country', 'state', 'zip', 'url', 'logo', 'enrolled_date', 'is_active' ]
    #template_name = 'vendors/vendors_list.html'  # Specify your own template name/location

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = Token.objects.get(user=self.request.user)
        context['token'] = token

        return context

class CompanyDetailView(GroupRequiredMixin, DetailView):
    group_required = [u"owner", u"auditor", u"administrator"]
    login_url = '/'
    model = Company
    template_name = 'companies/company_detail.html'
    fields = [ 'name', 'address1', 'address2', 'country', 'state', 'zip', 'url', 'logo', 'enrolled_date', 'is_active' ]
    def get_success_url(self):
        return reverse('company_list')

    def get_object(self, queryset=None):
        obj = Company.objects.filter(uuid=self.kwargs['uuid']).first()
        return obj

    def get_queryset(self):
        print("self kwarg id:" + self.kwargs['uuid'])
        queryset = Company.objects.filter(uuid=self.kwargs['uuid']).order_by('id')
        return queryset

class CompanyUpdateView(GroupRequiredMixin, UpdateView):
    group_required = [ u"owner", u"administrator"]
    login_url = '/'
    model = Company
    slug_url_kwarg = Company.uuid
    template_name = 'companies/company_update.html'
    #form_class = CompanyModifyForm
    fields = '__all__'

    def get_success_url(self):
            return reverse('company_detail')

    def get_object(self, queryset=None):
        obj = Company.objects.filter(uuid=self.kwargs['uuid']).first()
        return obj

    def get_queryset(self):
        print("self kwarg id:" + self.kwargs['uuid'])
        queryset = Company.objects.filter(uuid=self.kwargs['uuid']).order_by('id')
        return queryset

class CompanyDeleteView(GroupRequiredMixin, DeleteView):
    group_required = [ u"owner", u"administrator"]
    login_url = '/'
    model = Company
    slug_url_kwarg = Company.uuid
    #template_name = 'vendor_delete.html'
    def get_success_url(self):
            return reverse('company_list')

    def get_object(self, queryset=None):
        obj = Company.objects.filter(uuid=self.kwargs['uuid']).first()
        return obj

    def get_queryset(self):
        print("self kwarg id:" + self.kwargs['uuid'])
        queryset = Company.objects.filter(uuid=self.kwargs['uuid']).order_by('id')
        return queryset

class FormActionMixin(object):

    def post(self, request, *args, **kwargs):
        """Add 'Cancel' button redirect."""
        if "cancel" in request.POST:
            url = reverse('company_list')     # or e.g. reverse(self.get_success_url())
            return HttpResponseRedirect(url)
        else:
            return super(FormActionMixin, self).post(request, *args, **kwargs)

#class CompanyCreateView(BSModalCreateView):
class CompanyCreateView(GroupRequiredMixin, FormActionMixin, CreateView):
    group_required = [ u"owner", u"administrator" ]
#class CompanyCreateView(GroupRequiredMixin, CreateView):
    #group_required = [u"owner", u"administrator"]
    template_name = 'companies/company_new.html'
    form_class = NewCompanyForm
    #form_class = CrispyCompanyForm
    success_message = 'Success: Vendor was created.'
    success_url = reverse_lazy('company_list')

    def get_initial(self):
        #return {'Owner': self.kwargs['request.user']}


        return {'relationship_owner': self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.all()
        context['companies'] = companies
        return context

class SignUp(CreateView):
    #form_class = MyUserCreationForm
    form_class = RegisterForm #AddUserForm #PersonCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

#class Settings(CreateView):
#    form_class = UserProfileForm
#    #success_url = reverse_lazy('login')
#    template_name = 'settings.html'



class UserListView(GroupRequiredMixin, ListView):
    group_required = [u"owner", u"auditor", u"administrator"]
    login_url = '/'
    model = User
    context_object_name = 'user_list'   # your own name for the list as a template variable
    queryset = User.objects.all()
    fields = [ 'first_name', 'last_name', 'email', 'phone' ]
    paginate_by = 10
    #template_name = 'vendors/vendors_list.html'  # Specify your own template name/location
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = Token.objects.get(user=self.request.user)
        context['token'] = token
        return context


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_objectobjectobjectvalid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

#class UserCreateView(BSModalCreateView):
class UserCreateView(GroupRequiredMixin, CreateView):
    group_required = [ u"owner", u"administrator" ]
    login_url = '/'
    model = User
    #template_name = 'Framework_new.html'
    template_name = 'companies/user_new.html'
    #form_class = NewUserForm
    form_class = RegisterForm2
    #fields = ['Name', 'Vendor', 'Owner', 'StartDate', 'CompleteDate', 'Status', 'Frameworks']
    def get_success_url(self):
            return reverse('user_list')


class PersonFormActionMixin(object):

    def post(self, request, *args, **kwargs):
        """Add 'Cancel' button redirect."""
        if "cancel" in request.POST:
            url = reverse('user_list')     # or e.g. reverse(self.get_success_url())
            return HttpResponseRedirect(url)
        else:
            return super(PersonFormActionMixin, self).post(request, *args, **kwargs)

class PersonCreateView(GroupRequiredMixin, PersonFormActionMixin, CreateView):
    group_required = [u"owner", u"administrator"]
    template_name = 'companies/person_new.html'
    #generated_password  = User.objects.make_random_password(length=14, allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ1234567890!@#$%^&*()[]\{}|;:,./<>?") # zvk0hawf8m6394
    #initial = {'password1': generated_password, 'password2': generated_password}
    form_class = NewPersonForm
    groups = Group.objects.all()
    model = User
    #form_class = CrispyCompanyForm
    #success_message = 'Success: User was created.'
    success_url = reverse_lazy('user_list')

    #def get_initial(self):
    #    generated_password  = User.objects.make_random_password(length=14, allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ1234567890!@#$%^&*()[]\{}|;:,./<>?") # zvk0hawf8m6394
    #    print(generated_password)
    #    return {'password1': generated_password, 'password2': generated_password}
        #return {'relationship_owner': self.request.user}
    def form_valid(self, form):
        user_email=form.cleaned_data['email']

        subject = "Venchmark Account Creation Notification"
        message_html = ""
        message_html += "<html>Hello, " + form.cleaned_data['first_name'] + ", "
        message_html += "<p><p>      An account has been created for you in the Venchmark system. You can log into Venchmark at the link below. Please remember to reset your password once you log in. "
        message_html += "<p>                "
        message_html += "<p>                "
        message_html += "<p>                Password: " + str(form.cleaned_data['password1'])
        message_html += "<p>" + self.request.build_absolute_uri('/').strip("/") + "/people/login/"
        message_html += "</html>"
        from_email = self.request.user.email
        to_email = user_email
        send_mail(
            subject,
            message_html,
            from_email,
            recipient_list = [ to_email ]
        )
        #self.success_url = self.request.META.get('HTTP_REFERER')
        return super().form_valid(form)
    #        first_name = form.cleaned_data['first_name']
    #        last_name  = form.cleaned_data['last_name']
    #        email      = form.cleaned_data['email']
#from django.core.mail import send_mail
    #        subject = "Venchmark Account Creation Notificatoin"
    #        message = ""
    #        message += "Hello, " + first_name + ", "
    #        message += "      An account has been created for you in the Venchmark system. You can log into Venchmark at the link below. Please remember to reset your password once you log in. {% url 'login' %}"
    #        from_email = self.request.user.email
    #        to_email = email
    #        send_mail(
    #            subject,
    #            message,
    #            from_email,
    #            recipient_list = [ to_email ]
    #        )
    #    print("form valid - hit this function - in view")
        #self.object.groups.clear()
    #    groups = form.cleaned_data['groups']
    #    for group in groups:
    #        print("saving this group in user: " + str(group))
    #        self.object.groups.add(group)
    #    print("redirecting to " + str(self.request.META.get('HTTP_REFERER')))
    #    self.success_url = self.request.META.get('HTTP_REFERER') #self.request.POST.get('previous_page')
    #        return super().form_valid(form)

class UserCreateView2(GroupRequiredMixin, FormView):
    group_required = [ u"owner", u"administrator" ]
    login_url = '/'
#    model = User
    template_name = 'companies/user_new.html'
    form_class = RegisterForm2
    #fields = ['Name', 'Vendor', 'Owner', 'StartDate', 'CompleteDate', 'Status', 'Frameworks']
    def get_success_url(self):
            return reverse('user_list')




            #@receiver(post_save, sender=settings.AUTH_USER_MODEL)
            #def send_new_user_mail(sender, instance=None, **kwargs):
            #    user=instance
            #    #thisrequest=request
            #    subject = "Venchmark Account Creation Notificatoin"
            #    message = ""
            #    message += "Hello, " + user.first_name + ", "
            #    message += "      An account has been created for you in the Venchmark system. You can log into Venchmark at the link below. Please remember to reset your password once you log in. " #+ thisrequest.get_full_path()
            #    from_email = "no-reply@venchmark.com" #thisrequest.user.email
            #    to_email = user.email
            #    send_user_email(subject, message, from_email, to_email, request)

class UserUpdateView(GroupRequiredMixin, UpdateView):
    group_required = [ u"owner", u"administrator"]
    login_url = '/'
    model = User
    slug_url_kwarg = User.uuid
    template_name = 'companies/user_update.html'
    #form_class = CompanyModifyForm
    fields = '__all__'

    def get_success_url(self):
            return reverse('user_detail')

    def get_object(self, queryset=None):
        obj = User.objects.filter(uuid=self.kwargs['uuid']).first()
        return obj

    def get_queryset(self):
        #print("self kwarg id:" + self.kwargs['uuid'])
        queryset = User.objects.filter(uuid=self.kwargs['uuid']).order_by('id')
        return queryset

class UserFormActionMixin(object):

    def post(self, request, *args, **kwargs):

###### THIS CODE HERE IS FUCKED AND DOESN"T WORK....FIND CASE LOGIC AND APPLY IT
        """Add 'AddSource' button redirect."""
        if "cancel" in request.POST:
            url = reverse('user_list')     # or e.g. reverse(self.get_success_url())
            return HttpResponseRedirect(url)
        #elif "cancel" in request.POST:
        #    url = reverse('framework_list')     # or e.g. reverse(self.get_success_url())
        #    return HttpResponseRedirect(url)
        #elif "AddControls" in request.POST:
    #        slug_url_kwarg = Framework.uuid
    #        url = '/controls/' + str(self.kwargs['uuid'])    # or e.g. reverse(self.get_success_url())
    #        return HttpResponseRedirect(url)
        else:
            return super(UserFormActionMixin, self).post(request, *args, **kwargs)

class PersonUpdateView(GroupRequiredMixin, UserFormActionMixin, UpdateView):
#class PersonUpdateView(BSModalUpdateView):
    group_required = [ u"owner", u"administrator"]
    login_url = '/'
    model = User
    slug_url_kwarg = User.uuid
    template_name = 'companies/person_update_form.html'
    form_class = UpdatePersonForm
    success_url = reverse_lazy('user_list')
    #success_url = reverse('user_list')
    #fields = '__all__'

    #def get_success_url(self):
    #        return reverse('user_detail')

    def get_object(self, queryset=None):
        #obj = User.objects.filter(uuid=self.kwargs['uuid']).first()
        myUser = User.objects.get(pk=self.kwargs['uuid'])
        #print(myUser.first_name + " " + myUser.last_name)
        groups = myUser.groups.all()
        #for group in groups:
        #    print(group)
        #print(groups)
        #print("user belongs " + str(groups.count()) + " groups.")
        #for group in groups:
    #        print("retrieved group" + str(group))
        return myUser

    def form_valid(self, form):
        #self.object.groups.clear()
        #groups = form.cleaned_data['groups']
        #for group in groups:
        #    print("saving this group in user: " + str(group))
        #    user.object.groups.add(group)
        #self.success_url = self.request.META.get('HTTP_REFERER') #self.request.POST.get('previous_page')
        return super().form_valid(form)

    def get_initial(self):
        myUser = User.objects.get(pk=self.kwargs['uuid'])

        initial = super(PersonUpdateView, self).get_initial()
        try:
            groups = myUser.groups.all()
            #print(groups)
            #groups = self.object.groups.get()
        except:
            # exception can occur if the edited user has no groups
             #or has more than one group
            pass
        else:
            groups = Group.objects.all()
        return initial

class UserDetailView(GroupRequiredMixin, DetailView):
    group_required = [u"owner", u"auditor", u"administrator"]
    login_url = '/'
    model = User
    template_name = 'companies/user_detail.html'
    fields = "__all__"
    #fields = [ 'name', 'address1', 'address2', 'country', 'state', 'zip', 'url', 'logo', 'enrolled_date', 'is_active' ]
    def get_success_url(self):
        return reverse('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = Token.objects.get(user=self.request.user)
        context['token'] = token
        return context

    def get_object(self, queryset=None):
        obj = User.objects.filter(uuid=self.kwargs['uuid']).first()
        return obj

    def get_queryset(self):
        queryset = User.objects.filter(uuid=self.kwargs['uuid']).order_by('id')
        return queryset

class UserDeleteView(GroupRequiredMixin, DeleteView):
    group_required = [ u"owner", u"administrator"]
    login_url = '/'
    model = User
    slug_url_kwarg = User.uuid
    #template_name = 'vendor_delete.html'
    def get_success_url(self):
            return reverse('user_list')

    def get_object(self, queryset=None):
        obj = User.objects.filter(uuid=self.kwargs['uuid']).first()
        return obj

    def get_queryset(self):
        print("self kwarg id:" + self.kwargs['uuid'])
        queryset = User.objects.filter(uuid=self.kwargs['uuid']).order_by('id')
        return queryset

class CompanyUpdateView2(GroupRequiredMixin, FormActionMixin, UpdateView):
#class PersonUpdateView(BSModalUpdateView):
    group_required = [ u"owner", u"administrator"]
    login_url = '/'
    model = User
    slug_url_kwarg = Company.uuid
    template_name = 'companies/company_update_form.html'
    form_class = UpdateCompanyForm
    success_url = reverse_lazy('company_list')
    #fields = '__all__'

    #def get_success_url(self):
    #        return reverse('user_detail')

    def get_object(self, queryset=None):
        #obj = User.objects.filter(uuid=self.kwargs['uuid']).first()
        myCompany = Company.objects.get(pk=self.kwargs['uuid'])
        print("got object in companyupdateview2")
        #print(myUser.first_name + " " + myUser.last_name)
        #groups = myUser.groups.all()
        #for group in groups:
        #    print(group)
        #print(groups)
        #print("user belongs " + str(groups.count()) + " groups.")
        #for group in groups:
    #        print("retrieved group" + str(group))
        return myCompany

    def form_valid(self, form):
        print("form_valid!!!!")
        #self.object.groups.clear()
        #groups = form.cleaned_data['groups']
        #for group in groups:
        #    print("saving this group in user: " + str(group))
        #    user.object.groups.add(group)
        #self.success_url = '/companies/' #self.request.META.get('HTTP_REFERER') #self.request.POST.get('previous_page')
        return super().form_valid(form)

#class CompanyDeleteView2(GroupRequiredMixin, FormView):
class CompanyDeleteView2(GroupRequiredMixin, BSModalDeleteView):
    group_required = [ u"owner", u"administrator"]
    login_url = '/'
    model = Company
    slug_url_kwarg = Company.uuid
    template_name = 'companies/company_delete_form.html'
    success_message = 'Vendor Company Deleted Successfully.'
    success_url = '/companies/'
# self.request.META.get('HTTP_REFERER') #self.request.POST.get('previous_page')
    #def get_success_url(self):
    #        return reverse('company_list')

    def get_object(self, queryset=None):
        obj = Company.objects.filter(uuid=self.kwargs['uuid']).first()
        return obj

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        return kwargs

    def get_queryset(self):
    #    print("self kwarg id:" + self.kwargs['uuid'])
        queryset = Company.objects.filter(uuid=self.kwargs['uuid']) #.order_by('id')
        return queryset

    #def form_valid(self, form):
    #    company = self.get_object()
#        print("Deleting company: " + str(company))
    #    company.delete()
        #self.object.groups.clear()
        #groups = form.cleaned_data['groups']
        #for group in groups:
        #    print("saving this group in user: " + str(group))
        #    user.object.groups.add(group)
    #    self.success_url = self.request.META.get('HTTP_REFERER') #self.request.POST.get('previous_page')
    #    return super().form_valid(form)

    #def get_initial(self):
    #    success_url = self.request.META.get('HTTP_REFERER') #self.request.POST.get('previous_page')
    #    return success_url

class UserDeleteView2(GroupRequiredMixin, BSModalDeleteView):
    group_required = [ u"owner", u"administrator"]
    login_url = '/'
    model = User
    slug_url_kwarg = User.uuid
    template_name = 'companies/user_delete_form.html'
    success_message = 'User Deleted Successfully.'
    success_url = '/people/'

    #def get_success_url(self):
    #        return reverse('user_list')

    def get_object(self, queryset=None):
        obj = User.objects.filter(uuid=self.kwargs['uuid']).first()
        return obj

    def get_queryset(self):
    #    print("self kwarg id:" + self.kwargs['uuid'])
        queryset = User.objects.filter(uuid=self.kwargs['uuid']) #.order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        return kwargs

class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return User.objects.none()

        qs = User.objects.all()

        if self.q:
            qs = qs.filter(first_name__istartswith=self.q) | qs.filter(last_name__istartswith=self.q) | qs.filter(email__icontains=self.q)

        return qs


class CompanyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Company.objects.none()

        qs = Company.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class StatesAutocomplete(autocomplete.Select2QuerySetView):
    STATES = [
        ('Alabama', 'Alabama'),
        ('Alaska', 'Alaska'),
        ('Arizona', 'Arizona'),
        ('Arkansas', 'Arkansas'),
        ('California', 'California'),
        ('Colorado', 'Colorado'),
        ('Connecticut', 'Connecticut'),
        ('Delaware', 'Delaware'),
        ('Florida', 'Florida'),
        ('Georgia', 'Georgia'),
        ('Hawaii', 'Hawaii'),
        ('Idaho', 'Idaho'),
        ('Illinois', 'Illinois'),
        ('Indiana', 'Indiana'),
        ('Iowa', 'Iowa'),
        ('Kansas', 'Kansas'),
        ('Kentucky', 'Kentucky'),
        ('Louisiana', 'Louisiana'),
        ('Maine', 'Maine'),
        ('Maryland', 'Maryland'),
        ('Massachusetts', 'Massachusetts'),
        ('Michigan', 'Michigan'),
        ('Minnesota', 'Minnesota'),
        ('Mississippi', 'Mississippi'),
        ('Missouri', 'Missouri'),
        ('Montana', 'Montana'),
        ('Nebraska', 'Nebraska'),
        ('Nevada', 'Nevada'),
        ('New Hampshire', 'New Hampshire'),
        ('New Jersey', 'New Jersey'),
        ('New Mexico', 'New Mexico'),
        ('New York', 'New York'),
        ('North Carolina', 'North Carolina'),
        ('North Dakota', 'North Dakota'),
        ('Ohio', 'Ohio'),
        ('Oklahoma', 'Oklahoma'),
        ('Oregon', 'Oregon'),
        ('Pennsylvania', 'Pennsylvania'),
        ('South Carolina', 'South Carolina'),
        ('South Dakota', 'South Dakota'),
        ('Tennessee', 'Tennessee'),
        ('Texas', 'Texas'),
        ('Utah', 'Utah'),
        ('Vermont', 'Vermont'),
        ('Virginia', 'Virginia'),
        ('Washington', 'Washington'),
        ('Wisconsin', 'Wisconsin'),
        ('Wyoming', 'Wyoming'),
    ]

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return STATES

        qs = STATES #Company.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
