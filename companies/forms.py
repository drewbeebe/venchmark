#companies/forms.py
from dal import autocomplete
from django import forms

from tempus_dominus.widgets import DatePicker
from django.forms import ModelForm
#from django.contrib.auth.models import User as contribUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from bootstrap_modal_forms.forms import BSModalForm
from . models import Company, User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.http import HttpResponseRedirect
#from bootstrap_modal_forms.forms import BSModalForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import StrictButton
from .widgets import BootstrapDateTimePickerInput, BootstrapSelect

COUNTRIES = [
    ('United States', 'United States'),
    ('Afghanistan', 'Afghanistan'),
    ('Albania', 'Albania'),
    ('Algeria', 'Algeria'),
    ('Andorra', 'Andorra'),
    ('Angola', 'Angola'),
    ('Antigua & Deps', 'Antigua & Deps'),
    ('Argentina', 'Argentina'),
    ('Armenia', 'Armenia'),
    ('Australia', 'Australia'),
    ('Austria', 'Austria'),
    ('Azerbaijan', 'Azerbaijan'),
    ('Bahamas', 'Bahamas'),
    ('Bahrain', 'Bahrain'),
    ('Bangladesh', 'Bangladesh'),
    ('Barbados', 'Barbados'),
    ('Belarus', 'Belarus'),
    ('Belgium', 'Belgium'),
    ('Belize', 'Belize'),
    ('Benin', 'Benin'),
    ('Bhutan', 'Bhutan'),
    ('Bolivia', 'Bolivia'),
    ('Bosnia Herzegovina', 'Bosnia Herzegovina'),
    ('Botswana', 'Botswana'),
    ('Brazil', 'Brazil'),
    ('Brunei', 'Brunei'),
    ('Bulgaria', 'Bulgaria'),
    ('Burkina', 'Burkina'),
    ('Burundi', 'Burundi'),
    ('Cambodia', 'Cambodia'),
    ('Cameroon', 'Cameroon'),
    ('Canada', 'Canada'),
    ('Cape Verde', 'Cape Verde'),
    ('Central African Rep', 'Central African Rep'),
    ('Chad', 'Chad'),
    ('Chile', 'Chile'),
    ('China', 'China'),
    ('Colombia', 'Colombia'),
    ('Comoros', 'Comoros'),
    ('Congo', 'Congo'),
    ('Congo {Democratic Rep}', 'Congo {Democratic Rep}'),
    ('Costa Rica', 'Costa Rica'),
    ('Croatia', 'Croatia'),
    ('Cuba', 'Cuba'),
    ('Cyprus', 'Cyprus'),
    ('Czech Republic', 'Czech Republic'),
    ('Denmark', 'Denmark'),
    ('Djibouti', 'Djibouti'),
    ('Dominica', 'Dominica'),
    ('Dominican Republic', 'Dominican Republic'),
    ('East Timor', 'East Timor'),
    ('Ecuador', 'Ecuador'),
    ('Egypt', 'Egypt'),
    ('El Salvador', 'El Salvador'),
    ('Equatorial Guinea', 'Equatorial Guinea'),
    ('Eritrea', 'Eritrea'),
    ('Estonia', 'Estonia'),
    ('Ethiopia', 'Ethiopia'),
    ('Fiji', 'Fiji'),
    ('Finland', 'Finland'),
    ('France', 'France'),
    ('Gabon', 'Gabon'),
    ('Gambia', 'Gambia'),
    ('Georgia', 'Georgia'),
    ('Germany', 'Germany'),
    ('Ghana', 'Ghana'),
    ('Greece', 'Greece'),
    ('Grenada', 'Grenada'),
    ('Guatemala', 'Guatemala'),
    ('Guinea', 'Guinea'),
    ('Guinea-Bissau', 'Guinea-Bissau'),
    ('Guyana', 'Guyana'),
    ('Haiti', 'Haiti'),
    ('Honduras', 'Honduras'),
    ('Hungary', 'Hungary'),
    ('Iceland', 'Iceland'),
    ('India', 'India'),
    ('Indonesia', 'Indonesia'),
    ('Iran', 'Iran'),
    ('Iraq', 'Iraq'),
    ('Ireland', 'Ireland'),
    ('Israel', 'Israel'),
    ('Italy', 'Italy'),
    ('Ivory Coast', 'Ivory Coast'),
    ('Jamaica', 'Jamaica'),
    ('Japan', 'Japan'),
    ('Jordan', 'Jordan'),
    ('Kazakhstan', 'Kazakhstan'),
    ('Kenya', 'Kenya'),
    ('Kiribati', 'Kiribati'),
    ('Korea North', 'Korea North'),
    ('Korea South', 'Korea South'),
    ('Kosovo', 'Kosovo'),
    ('Kuwait', 'Kuwait'),
    ('Kyrgyzstan', 'Kyrgyzstan'),
    ('Laos', 'Laos'),
    ('Latvia', 'Latvia'),
    ('Lebanon', 'Lebanon'),
    ('Lesotho', 'Lesotho'),
    ('Liberia', 'Liberia'),
    ('Libya', 'Libya'),
    ('Liechtenstein', 'Liechtenstein'),
    ('Lithuania', 'Lithuania'),
    ('Luxembourg', 'Luxembourg'),
    ('Macedonia', 'Macedonia'),
    ('Madagascar', 'Madagascar'),
    ('Malawi', 'Malawi'),
    ('Malaysia', 'Malaysia'),
    ('Maldives', 'Maldives'),
    ('Mali', 'Mali'),
    ('Malta', 'Malta'),
    ('Marshall Islands', 'Marshall Islands'),
    ('Mauritania', 'Mauritania'),
    ('Mauritius', 'Mauritius'),
    ('Mexico', 'Mexico'),
    ('Micronesia', 'Micronesia'),
    ('Moldova', 'Moldova'),
    ('Monaco', 'Monaco'),
    ('Mongolia', 'Mongolia'),
    ('Montenegro', 'Montenegro'),
    ('Morocco', 'Morocco'),
    ('Mozambique', 'Mozambique'),
    ('Myanmar, {Burma}', 'Myanmar, {Burma}'),
    ('Namibia', 'Namibia'),
    ('Nauru', 'Nauru'),
    ('Nepal', 'Nepal'),
    ('Netherlands', 'Netherlands'),
    ('New Zealand', 'New Zealand'),
    ('Nicaragua', 'Nicaragua'),
    ('Niger', 'Niger'),
    ('Nigeria', 'Nigeria'),
    ('Norway', 'Norway'),
    ('Oman', 'Oman'),
    ('Pakistan', 'Pakistan'),
    ('Palau', 'Palau'),
    ('Panama', 'Panama'),
    ('Papua New Guinea', 'Papua New Guinea'),
    ('Paraguay', 'Paraguay'),
    ('Peru', 'Peru'),
    ('Philippines', 'Philippines'),
    ('Poland', 'Poland'),
    ('Portugal', 'Portugal'),
    ('Qatar', 'Qatar'),
    ('Romania', 'Romania'),
    ('Russian Federation', 'Russian Federation'),
    ('Rwanda', 'Rwanda'),
    ('St Kitts & Nevis', 'St Kitts & Nevis'),
    ('St Lucia', 'St Lucia'),
    ('Saint Vincent & the Grenadines', 'Saint Vincent & the Grenadines'),
    ('Samoa', 'Samoa'),
    ('San Marino', 'San Marino'),
    ('Sao Tome & Principe', 'Sao Tome & Principe'),
    ('Saudi Arabia', 'Saudi Arabia'),
    ('Senegal', 'Senegal'),
    ('Serbia', 'Serbia'),
    ('Seychelles', 'Seychelles'),
    ('Sierra Leone', 'Sierra Leone'),
    ('Singapore', 'Singapore'),
    ('Slovakia', 'Slovakia'),
    ('Slovenia', 'Slovenia'),
    ('Solomon Islands', 'Solomon Islands'),
    ('Somalia', 'Somalia'),
    ('South Africa', 'South Africa'),
    ('South Sudan', 'South Sudan'),
    ('Spain', 'Spain'),
    ('Sri Lanka', 'Sri Lanka'),
    ('Sudan', 'Sudan'),
    ('Suriname', 'Suriname'),
    ('Swaziland', 'Swaziland'),
    ('Sweden', 'Sweden'),
    ('Switzerland', 'Switzerland'),
    ('Syria', 'Syria'),
    ('Taiwan', 'Taiwan'),
    ('Tajikistan', 'Tajikistan'),
    ('Tanzania', 'Tanzania'),
    ('Thailand', 'Thailand'),
    ('Togo', 'Togo'),
    ('Tonga', 'Tonga'),
    ('Trinidad & Tobago', 'Trinidad & Tobago'),
    ('Tunisia', 'Tunisia'),
    ('Turkey', 'Turkey'),
    ('Turkmenistan', 'Turkmenistan'),
    ('Tuvalu', 'Tuvalu'),
    ('Uganda', 'Uganda'),
    ('Ukraine', 'Ukraine'),
    ('United Arab Emirates', 'United Arab Emirates'),
    ('United Kingdom', 'United Kingdom'),
    ('Uruguay', 'Uruguay'),
    ('Uzbekistan', 'Uzbekistan'),
    ('Vanuatu', 'Vanuatu'),
    ('Vatican City', 'Vatican City'),
    ('Venezuela', 'Venezuela'),
    ('Vietnam', 'Vietnam'),
    ('Yemen', 'Yemen'),
    ('Zambia', 'Zambia'),
    ('Zimbabwe', 'Zimbabwe'),

]

STATES = [
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
]

CITIES = [
    ('MIDDLETOWN', 'Middletown')
]

RISK_RATINGS = [
    ('LOW', 'Low'),
    ('MODERATE', 'Moderate'),
    ('HIGH', 'High')
]

SENSITIVITIES = [
    ('LOW', 'Low'),
    ('MODERATE', 'Moderate'),
    ('HIGH', 'High')
]

class CompanyAddForm(ModelForm):
    class Meta:
        model = Company
        #exclude = ['id']
        fields = ['name', 'address1', 'address2', 'country', 'city', 'state', 'zip', 'url', 'logo', 'enrolled_date', 'is_active', 'risk_rating']

#class VendorForm(ModelForm):
#    class Meta:
#        model = Company
#        #exclude = ['id']
#        fields = ['name', 'address1', 'address2', 'country', 'city', 'state', 'zip', 'url', 'logo', 'enrolled_date', 'is_active', 'risk_rating']


class CompanyListForm(forms.Form):
    class Meta:
        model = Company
        fields = ['CompanyName', 'CompanyURL']

class CompanyDetailForm(forms.Form):
    class Meta:
        model = Company
        #fields = ['CompanyName', 'CompanyURL']

class CompanyModifyForm(forms.Form):
    class Meta:
        model = Company
        exclude = ( 'employee', )
        fields = ['name', 'address1', 'address2', 'country', 'city', 'state', 'zip', 'url', 'logo', 'enrolled_date', 'is_active', 'risk_rating', 'relationship_owner' ]

#class NewCompanyForm(BSModalForm):
#    name        = forms.TextInput(attrs={'size': 100, 'title': 'Company Name'})
#    is_actiive  = forms.CheckboxInput
#    address1        = forms.TextInput(attrs={'size': 100, 'title': 'Company Address'})
#    address2        = forms.TextInput(attrs={'size': 50, 'title': 'Suite No.'})
#    class Meta:
#        model = Company
#        #exclude = ['id']
#        fields = ['name', 'address1', 'address2', 'country', 'city', 'state', 'zip', 'url', 'logo', 'enrolled_date', 'is_active', 'risk_rating', 'relationship_owner' ]
#
#        #Owner = forms.TypedChoiceField(initial=request.user)
#        def get_initial(self):
#        #return {'Owner': self.kwargs['request.user']}
#            return {'relationship_owner': self.request.user}
#
#        def __init__(self, request, *args, **kwargs):
#            super(NewCompanyForm, self).__init__(*args, **kwargs)

class NewCompanyForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '75', 'placeholder': 'Company Name'}))
    address1 = forms.CharField(widget=forms.TextInput(attrs={'size': '75', 'placeholder': '123 Main Street'}))
    address2 = forms.CharField(widget=forms.TextInput(attrs={'size': '75', 'placeholder': 'Suite 500'}), required=False)
    country = forms.ChoiceField(choices=COUNTRIES, widget=BootstrapSelect())
    city = forms.CharField(widget=forms.TextInput(attrs={'size': '75', 'placeholder': 'City'}))
    state = forms.ChoiceField(choices=STATES, widget=BootstrapSelect())
    #state = forms.ChoiceField(
    #    widget=autocomplete.ModelSelect2(url='states-autocomplete'),
    #    label="State"
    #)
    zip = forms.CharField(widget=forms.TextInput(attrs={'size': '25', 'placeholder': 'Zip Code'}))
    url = forms.CharField(widget=forms.TextInput(attrs={'size': '75', 'placeholder': 'http://www.example.com'}),required=False)
    logo = forms.CharField(widget=forms.TextInput(attrs={'size': '75', 'placeholder': 'http://www.example.com/example_logo.jpg'}),required=False)
    #enrolled_date = forms.DateTimeField(
    #    input_formats=['%d/%m/%Y %H:%M'],
    #    widget=BootstrapDateTimePickerInput()
    #    )
    relationship_owner = forms.ModelChoiceField(User.objects.all(), widget=BootstrapSelect())
    relationship_owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user-autocomplete'),
        label="Relationship Owner"
    )
    risk_rating = forms.ChoiceField(choices=RISK_RATINGS, widget=BootstrapSelect())
    data_sensitivity_rating = forms.ChoiceField(choices=SENSITIVITIES, widget=BootstrapSelect())
    is_active = forms.CheckboxInput()
    is_vendor = forms.CheckboxInput()

    class Meta:
        model = Company
        #exclude = ['id']
        #fields = [ 'name', 'vendor', 'owner', 'vendor_contact', 'auditor', 'analyst', 'status', 'frameworks' ]
        fields = [ 'name', 'address1', 'address2', 'country', 'city', 'state', 'zip', 'url', 'logo', 'enrolled_date', 'relationship_owner', 'risk_rating', 'data_sensitivity_rating', 'is_active', 'is_vendor' ]
        widgets = {
            'enrolled_date': DatePicker(
                options={
                    'format': 'MM/DD/YYYY'
                },
                attrs={
                    'append': 'fa fa-calendar',
                },
            )
        }
        labels = {
            'is_vendor': 'Is this company a Vendor?',
            'is_active': 'Is the relationship with this Vendor Active?',
        }

    def get_initial(self):
        return {'relationship_owner': self.request.user}


    def __init__(self, *args, **kwargs):
        super(NewCompanyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(

                #Column('name', css_class='form-group mb-4'),
                #Column('relationship_owner', css_class='form-group col-md-4 mb-0'),
                HTML(
                '''
                <div  class="form-row form-row justify-content-md-center" >
                  <div  class="col form-group mb-4" >
                     <div id="div_id_name" class="form-group">
                       <label for="id_name" class=" requiredField">Name<span class="asteriskField">*</span> </label>
                       <div class="autocomplete">
                            <input type="text" name="name" size="125" placeholder="Company Name" class="textinput textInput form-control" required id="id_name">
                       </div>
                      </div>
                   </div>
                </div>
                '''
                ),
                #css_class='form-row justify-content-md-center'
            ),
            Row(
                #Column('address1', css_class='form-group col-md-8 mb-0'),
                Column('address1', css_class='form-group mb-4'),
                css_class='form-row justify-content-md-center'
            ),
            Row(
                #Column('address2', css_class='form-group col-md-8 mb-0'),
                Column('address2', css_class='form-group mb-4'),
                css_class='form-row justify-content-md-center'
            ),
            Row(
                #Column('city', css_class='form-group col-md-4 mb-0'),
                #Column('country', css_class='form-group col-md-4 mb-0'),
                #Column('state', css_class='form-group col-md-4 mb-0'),
                #Column('zip', css_class='form-group col-md-4 mb-0'),
                Column('city', css_class='form-group col- mb-0'),
                Column('state', css_class='form-group col- mb-0'),
                Column('zip', css_class='form-group col- mb-0'),
                Column('country', css_class='form-group col- mb-0'),
                css_class='form-row justify-content-md-center'
            ),
            Row(
                Column('url', css_class='form-group mb-4'),
                css_class='form-row justify-content-md-center'
            ),
            Row(
                Column('logo', css_class='form-group mb-4'),
                css_class='form-row justify-content-md-center'
            ),
            Row(
                Column('risk_rating', css_class='form-group col-md-4 mb-0'),
                Column('data_sensitivity_rating', css_class='form-group col-md-4 mb-0'),
                Column('relationship_owner', css_class='form-group col-md-4 mb-0'),
                css_class='form-row justify-content-md-center',
            ),
            Row(
                Column('enrolled_date', css_class='form-group col-md-4 mb-0'),
                Column('is_active', css_class='form-group col-md-4 mb-0'),
                Column('is_vendor', css_class='form-group col-md-4 mb-0'),
                css_class='form-row ',
            ),
            #Row(
                #Column('risk_rating', css_class='form-group col-md-4 mb-0'),
                #Column('data_sensitivity_rating', css_class='form-group col-md-4 mb-0'),

        #        Column('is_active', css_class='form-group col-md-4 mb-0'),
        #        Column('is_vendor', css_class='form-group col-md-4 mb-0'),
        #        css_class='form-row justify-content-md-center',
        #    ),


            #Submit('submit', 'Create Vendor')
        )
        self.helper.add_input(Submit('submit', 'Create Vendor'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger justify-content-md-center',
            formnovalidate='formnovalidate',
            )
        )


class CrispyCompanyForm(BSModalForm):
    class Meta:
        model = Company
        fields = ['name', 'address1', 'address2', 'country', 'city', 'state', 'zip', 'url', 'logo', 'enrolled_date', 'is_active', 'risk_rating', 'relationship_owner' ]
    def __init__(self, instance, request, *args, **kwargs):
        super(CrispyCompanyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'create-company'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-2'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.layout = Layout(
            'name', 'address1',
            'address2',
            'country',
            'city',
            'state',
            'zip',
            'url',
            'logo',
            'enrolled_date',
            'is_active',
            'risk_rating',
            'relationship_owner',
        )

        self.helper.add_input(Submit('submit', 'Submit'))
    def get_initial(self):
        #return {'Owner': self.kwargs['request.user']}
        return {'relationship_owner': self.request.user}

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class RegisterForm2(forms.Form):
    email       = forms.CharField(label="E-mail", required=True)
    password1   = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)
    password2   = forms.CharField(label="Confirm password", widget=forms.PasswordInput)
    admin       = forms.BooleanField(label="Administrator", widget=forms.CheckboxInput)
    owner       = forms.BooleanField(label="Relationship Owner", widget=forms.CheckboxInput)
    analyst     = forms.BooleanField(label="Analyst", widget=forms.CheckboxInput)
    auditor     = forms.BooleanField(label="Auditor", widget=forms.CheckboxInput)
    vendor      = forms.BooleanField(label="Vendor", widget=forms.CheckboxInput)

    helper      = FormHelper()
    helper.form_method  = 'POST'
    helper.add_input(Submit('Create User', 'Create User', css_class='btn-primary'))


    class Meta:
        model = User
        fields = ('email', 'admin', 'owner', 'analyst', 'auditor', 'vendor')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm2, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class NewPersonForm(forms.ModelForm):
    email               = forms.CharField(widget=forms.TextInput(attrs={'size': '75', 'placeholder': 'Email'}), required=True)
    #email               = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    #password            = forms.CharField(widget=forms.PasswordInput())
    first_name          = forms.CharField(widget=forms.TextInput(attrs={'size': '75','placeholder': 'First Name'}), required=False)
    last_name           = forms.CharField(widget=forms.TextInput(attrs={'size': '75','placeholder': 'Last Name'}), required=False)
    #usercompany         = forms.Select()
    #usercompany         = forms.ModelChoiceField(label="Company", queryset=Company.objects.all(), widget=forms.Select, required=True)
    usercompany         = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=autocomplete.ModelSelect2(url='company-autocomplete'),
        label="Company"
    )
    groups              = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple, label="Choose the User's Roles:", required=True)
#    password            = forms.CharField(widget=forms.PasswordInput)
    #is_superuser = forms.ChoiceField(widget=forms.CheckboxInput, label="Is this user a superuser?", required=False)
    password1   = forms.CharField(label="Password", required=True, widget=forms.TextInput) #initial=generated_password)
    password2   = forms.CharField(label="Confirm password", widget=forms.TextInput)

    class Meta:
        model = User
        #exclude = ['id']
        #fields = [ 'question', 'answer' ]
        #fields = [ 'answer' ]
        #fields = [ 'first_name', 'last_name', 'email', 'usercompany', 'groups', 'password1', 'password2' ]
        fields = [ 'first_name', 'last_name', 'email', 'usercompany', 'groups', 'password1', 'password2' ]
        labels = {
            'usercompany': ('Company'),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(NewPersonForm, self).save(commit=False)

        print("superuser: " + str(user.is_superuser))


        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        for selected_group in self.cleaned_data["groups"]:
            print(selected_group)
            user.groups.add(selected_group)
        if commit:
            user.save()

        return user
        #widgets = [ 'groups': forms.CheckBoxSelectMultiple()]
        #widgets = ['groups': forms.CheckboxSelectMultiple ]

#        # Check that the two password entries match
#        password1 = self.cleaned_data.get("password1")
#        password2 = self.cleaned_data.get("password2")
#        if password1 and password2 and password1 != password2:
#            raise forms.ValidationError("Passwords don't match")
#        return password2

#    def save(self, commit=True):
#        user = super(UpdatePersonForm, self).save(commit=False)
#        user.set_password(self.cleaned_data["password1"])
#        if commit:
#            user.save()
#        return user
#
    def __init__(self, *args, **kwargs):
        super(NewPersonForm, self).__init__(*args, **kwargs)

        generated_password  = User.objects.make_random_password(length=14, allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ1234567890!@#$%^&*()[]\{}|;:,./<>?") # zvk0hawf8m6394
        #print(generated_password)
        self.fields['password1'].initial = generated_password
        self.fields['password2'].initial = generated_password
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                #Column('email', css_class='form-group col-md-8 mb-0'),
                Column('email', css_class='form-group mb-4'),
                css_class='form-row justify-content-md-center'
            ),
            Row(
                Column('usercompany', css_class='form-group col- mb-0'),
                #Column('is_superuser', css_class='form-group col- mb-0'),
                #Column('start_date', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                #Column('city', css_class='form-group col-md-6 mb-0'),
                #Column('state', css_class='form-group col-md-4 mb-0'),
                #Column('zip_code', css_class='form-group col-md-2 mb-0'),
                Column('first_name', css_class='form-group col- mb-0'),
                Column('last_name', css_class='form-group col- mb-0'),

                css_class='form-row'
            ),

            Row(
                Column('password1', css_class='form-group col- mb-0', initial=generated_password),
                Column('password2', css_class='form-group col- mb-0', initial=generated_password),
            ),
            Row(
                #Column('usercompany', css_class='form-group col- mb-0'),
                Column('groups', css_class='form-group col- mb-0'),
                #Column('start_date', css_class='form-group col-md-4 mb-0'),
            ),
            #Submit('submit', 'Create Assessment')
        )
        self.helper.add_input(Submit('submit', 'Create User'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )




#class NewPersonForm(BSModalForm):
#class NewPersonForm(BSModalForm):
#class NewPersonForm(forms.ModelForm):
#    email               = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    #password            = forms.CharField(widget=forms.PasswordInput())
#    first_name          = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
#    last_name           = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
#    password1   = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)
#    password2   = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    #first_name          = forms.TextInput(attrs={'size': 100, 'title': 'First Name'})
    #last_name           = forms.TextInput(attrs={'size': 100, 'title': 'Last Name'})
    #email               = forms.TextInput(attrs={'size': 100, 'title': 'Email'})
#    usercompany         = forms.Select()
    #group               = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
#    groups               = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False, label='Groups', widget=forms.CheckboxSelectMultiple)
    #password1           = forms.CharField(label='Password', widget=forms.PasswordInput)
    #password2           = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    #groups              = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Choose the User's Roles:")
#    class Meta:
#        model = User
        #exclude = ['id']
#        fields = ['first_name', 'last_name', 'email', 'usercompany', ] #'address1', 'address2', 'country', 'city', 'state', 'zip', 'url', 'logo', 'enrolled_date', 'is_active', 'risk_rating', 'relationship_owner' ]
#
#    def form_valid(self, form):
#        print("form was valid --- entering this function - form")
#        self.object.groups.clear()
#        groups = form.cleaned_data['groups']
#        for group in groups:
#            self.object.groups.add(group)
#        return super(NewPersonForm, self).form_valid(form)

#    def clean_password2(self):
#        # Check that the two password entries match
#        password1 = self.cleaned_data.get("password1")
#        password2 = self.cleaned_data.get("password2")
#        if password1 and password2 and password1 != password2:
#            raise forms.ValidationError("Passwords don't match")
#        return password2

#    def save(self, commit=True):
#        user_instance = super(NewPersonForm, self).save(commit=False)
##        if commit:
#            user_instance.save()
#        #user_instance.user_permissions.set(self.cleaned_data.get('user_permissions'))
#        user_instance.groups.set(self.cleaned_data.get('groups'))
        #user = super(NewPersonForm, self).save(commit=False)
        #        user.set_password(self.cleaned_data["password1"])
        #        if commit:
        #            user.save()
#        return user_instance
#    def clean_password2(self):
#        # Check that the two password entries match
#        password1 = self.cleaned_data.get("password1")
#        password2 = self.cleaned_data.get("password2")
#        if password1 and password2 and password1 != password2:
#            raise forms.ValidationError("Passwords don't match")
#        return password2

#    def form_valid(self, form):
#        # This method is called when valid form data has been POSTed.
#        # It should return an HttpResponse.
#        user = form.save()
#        for group in self.groups:
#            user.groups.add(group)
#        return super().form_valid(form)


#    def save(self, commit=True):
#        # Save the provided password in hashed format
#        user = super(NewPersonForm, self).save(commit=False)
#        user.set_password(self.cleaned_data["password1"])
#        if commit:
#            user.save()
#        return user
        #Owner = forms.TypedChoiceField(initial=request.user)
        #def get_initial(self):
        #return {'Owner': self.kwargs['request.user']}
            #return {'relationship_owner': self.request.user}

        #def __init__(self, request, *args, **kwargs):
        #    super(NewPersonForm, self).__init__(*args, **kwargs)
#class UpdatePersonForm(BSModalForm):
#    first_name          = forms.TextInput(attrs={'size': 100, 'title': 'First Name'})
#    last_name           = forms.TextInput(attrs={'size': 100, 'title': 'Last Name'})
#    email               = forms.TextInput(attrs={'size': 100, 'title': 'Email'})
#    usercompany         = forms.Select()
#    group               = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
#    group               = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
#
#    class Meta:
#        model = User
#        #exclude = ['id']
#        fields = "__all__"
        #fields = ['first_name', 'last_name', 'email', 'usercompany', ]

class UpdatePersonForm(forms.ModelForm):
    email               = forms.CharField(widget=forms.TextInput(attrs={'size': '75', 'placeholder': 'Email'}))
    #email               = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    #password            = forms.CharField(widget=forms.PasswordInput())
    first_name          = forms.CharField(widget=forms.TextInput(attrs={'size': '75','placeholder': 'First Name'}))
    last_name           = forms.CharField(widget=forms.TextInput(attrs={'size': '75','placeholder': 'Last Name'}))
    usercompany         = forms.Select()
    groups              = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple, label="Choose the User's Roles:")
#    password            = forms.CharField(widget=forms.PasswordInput)
    #password1   = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)
    #password2   = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        #exclude = ['id']
        #fields = [ 'question', 'answer' ]
        #fields = [ 'answer' ]
        #fields = [ 'first_name', 'last_name', 'email', 'usercompany', 'groups', 'password1', 'password2' ]
        fields = [ 'first_name', 'last_name', 'email', 'usercompany', 'groups', ]
        labels = {
            'usercompany': ('Company'),
        }
        #widgets = [ 'groups': forms.CheckBoxSelectMultiple()]
        #widgets = ['groups': forms.CheckboxSelectMultiple ]

    #def clean_password2(self):
        # Check that the two password entries match
    #    password1 = self.cleaned_data.get("password1")
    #    password2 = self.cleaned_data.get("password2")
    #    if password1 and password2 and password1 != password2:
    #        raise forms.ValidationError("Passwords don't match")
    #    return password2

    #def save(self, commit=True):
    #    user = super(UpdatePersonForm, self).save(commit=False)
    #    user.set_password(self.cleaned_data["password1"])
    #    if commit:
    #        user.save()
    #    return user

    def __init__(self, *args, **kwargs):
        super(UpdatePersonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-8 mb-0'),

                css_class='form-row'
            ),
            Row(
                #Column('city', css_class='form-group col-md-6 mb-0'),
                #Column('state', css_class='form-group col-md-4 mb-0'),
                #Column('zip_code', css_class='form-group col-md-2 mb-0'),
                Column('first_name', css_class='form-group col-md-4 mb-0'),
                Column('last_name', css_class='form-group col-md-4 mb-0'),

                css_class='form-row'
            ),
            Row(
                Column('usercompany', css_class='form-group col-md-4 mb-0'),
                Column('groups', css_class='form-group col-md-4 mb-0'),
                #Column('start_date', css_class='form-group col-md-4 mb-0'),
            ),
            #Row(
            #    Column('password1', css_class='form-group col-md-4 mb-0'),
        #        Column('password2', css_class='form-group col-md-4 mb-0'),
        #    ),
            #Submit('submit', 'Create Assessment')
        )
        self.helper.add_input(Submit('submit', 'Update User'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )
#class UpdatePersonForm(forms.ModelForm):
##class UpdatePersonForm(BSModalForm):

#    email               = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
#    #password            = forms.CharField(widget=forms.PasswordInput())
#    first_name          = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
#    last_name           = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
#    usercompany         = forms.Select()
#    groups              = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple, label="Choose the User's Roles:")
##    password            = forms.CharField(widget=forms.PasswordInput)
##    password2   = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

#    class Meta:
#        model = User
        #exclude = ['id']
        #fields = [ 'question', 'answer' ]
        #fields = [ 'answer' ]
#        fields = [ 'first_name', 'last_name', 'email', 'usercompany', 'groups', 'password1', 'password2' ]
#        labels = {
#            'usercompany': ('Company'),
#        }
        #widgets = [ 'groups': forms.CheckBoxSelectMultiple()]
        #widgets = ['groups': forms.CheckboxSelectMultiple ]

#    def clean_password2(self):
#        # Check that the two password entries match
#        password1 = self.cleaned_data.get("password1")
#        password2 = self.cleaned_data.get("password2")
#        if password1 and password2 and password1 != password2:
#            raise forms.ValidationError("Passwords don't match")
#        return password2
#
#    def save(self, commit=True):
#        user = super(UpdatePersonForm, self).save(commit=False)
#        user.set_password(self.cleaned_data["password1"])
#        if commit:
#            user.save()
#        return user

#    def __init__(self, *args, **kwargs):
#        super(UpdatePersonForm, self).__init__(*args, **kwargs)
#        self.helper = FormHelper(self)
#        self.helper.form_class = 'form-horizontal'
#        self.helper.label_class = 'col-lg-2'
#        self.helper.field_class = 'col-lg-8'
#        self.helper.layout = Layout(
#            'first_name',
#            'last_name',
#            'email',
#            'password',
#            'usercompany',
#            'groups',
#
#            StrictButton('Update User', css_class='btn-default'),
#        )

class UpdateCompanyForm(forms.ModelForm):
    relationship_owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user-autocomplete'),
        label="Relationship Owner"
    )
    state = forms.ChoiceField(choices=STATES, widget=BootstrapSelect())
    risk_rating = forms.ChoiceField(choices=RISK_RATINGS, widget=BootstrapSelect())
    data_sensitivity_rating = forms.ChoiceField(choices=SENSITIVITIES, widget=BootstrapSelect())

    class Meta:
        model = Company
        #exclude = ['id']
        #fields = [ 'question', 'answer' ]
        #fields = [ 'answer' ]
        fields = ['name', 'address1', 'address2', 'country', 'city', 'state', 'zip', 'url', 'logo', 'enrolled_date', 'is_active', 'is_vendor', 'risk_rating', 'data_sensitivity_rating', 'relationship_owner' ]
        #labels = {
        #    'usercompany': ('Company'),
        #}
    def __init__(self, *args, **kwargs):
        super(UpdateCompanyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col- mb-4'),
                css_class='form-row'
            ),
            Row(
                Column('address1', css_class='form-group col- mb-4'),
                css_class='form-row'
            ),
            Row(
                Column('address2', css_class='form-group col- mb-4'),
                css_class='form-row'
            ),
            Row(
                #Column('city', css_class='form-group col-md-6 mb-0'),
                #Column('state', css_class='form-group col-md-4 mb-0'),
                #Column('zip_code', css_class='form-group col-md-2 mb-0'),
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('zip', css_class='form-group col-md-4 mb-0'),

                css_class='form-row'
            ),
            Row(
                Column('url', css_class='form-group col- mb-4'),
                css_class='form-row'
            ),
            Row(
                Column('logo', css_class='form-group col- mb-4'),
                css_class='form-row'
            ),
            Row(
                Column('risk_rating', css_class='form-group col-md-4 mb-0'),
                Column('data_sensitivity_rating', css_class='form-group col-md-4 mb-0'),
                Column('relationship_owner', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('is_active', css_class='form-group col-md-4 mb-0'),
                Column('is_vendor', css_class='form-group col-md-4 mb-0'),
            ),
            #Submit('submit', 'Create Vendor')
        )
        self.helper.add_input(Submit('submit', 'Update Vendor'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )
