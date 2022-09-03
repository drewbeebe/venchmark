import datetime
import uuid
from . import cipher

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, validate_email, EmailValidator
from django.utils import timezone
#from people.models import Person
#from users.models import MyCustomUser
from django.core.mail import send_mail
from .utils import send_user_email

#encryption Import
from django.db.models.fields import CharField, AutoField

##imports for People
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .managers import UserManager, CompanyManager
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import hashers

### classes for re-formatting models below

# EncryptedField
class EnField(CharField):
    def from_db_value(self, value, expression, connection):
        """ Decrypt the data for display in Django as normal. """
        return cipher.decrypt(value)
    def get_prep_value(self, value):
        """ Encrypt the data when saving it into the database. """
        return cipher.encrypt(value)

# AutoFieldNonPrimary
class AutoFieldNonPrimary(AutoField):

    def _check_primary_key(self):
        if self.primary_key:
            return [
                checks.Error(
                    "AutoFieldNonPrimary must not set primary_key=True.",
                    obj=self,
                    id="fields.E100",
                )
            ]
        else:
            return []

#class User(AbstractBaseUser, PermissionsMixin):
#    objects = CustomUserManager()
#    email = models.EmailField(
#        verbose_name=_('email address'), max_length=255, unique=True
#    )
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
#    order_id = models.IntegerField(default=1)
#    first_name = models.CharField(_('first name'), max_length=30, blank=True)
#    last_name = models.CharField(_('last name'), max_length=150, blank=True)
#    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this User.', editable=False, unique=True)
#    vendor = models.ManyToManyField('Company', through='CompanyUsers', blank=True)
#    is_active = models.BooleanField(
#        _('active'),
#        default=True,
#        help_text=_(
#            'Designates whether this user should be treated as active. '
#            'Unselect this instead of deleting accounts.'
#        ),
#    )
#    is_staff = models.BooleanField(
#        _('staff status'),
#        default=False,
#        help_text=_(
#            'Designates whether the user can log into this admin site.'
#        ),
#    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

#    date_joined = models.DateTimeField(
#        _('date joined'), default=timezone.now
#    )



#    USERNAME_FIELD = 'email'
#    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

#    def get_full_name(self):
#        """
#        Return the first_name plus the last_name, with a space in between.
#        """
#        full_name = '%s %s' % (self.first_name, self.last_name)
#        return full_name.strip()

#    def __str__(self):
#        return '{} <{}>'.format(self.get_full_name(), self.email)

#    def has_perm(self, perm, obj=None):
#        """
#        "Does the user have a specific permission?"
#        """
#        # Simplest possible answer: Yes, always
#        return True

#    def has_module_perms(self, app_label):
#        """
#        "Does the user have permissions to view the app `app_label`?"
#        """
#        # Simplest possible answer: Yes, always
#        return True

#    @receiver(post_save, sender=settings.AUTH_USER_MODEL)

#    def create_auth_token(sender, instance=None, created=False, **kwargs):
#        if created:
#            Token.objects.create(user=instance)
#
#    def save(self, *args, **kwargs):
#    # This means that the model isn't saved to the database yet
#        if self._state.adding:

            # Get the maximum display_id value from the database
#            last_id = User.objects.all().aggregate(largest=models.Max('order_id'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
#            if last_id is not None:
#                self.order_id = last_id + 1
#        super(User, self).save(*args, **kwargs)

class User(AbstractBaseUser):
    order_id = models.IntegerField(default=1)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this User.', editable=False, unique=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    usercompany = models.ManyToManyField('Company', through='CompanyUsers', blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=False,
    )
    is_active = models.BooleanField(default=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    #active = models.BooleanField(default=True, blank=True)
    #staff = models.BooleanField(default=False, blank=True) # a admin user; non super-user
    #admin = models.BooleanField(default=False, blank=True) # a superuser
    #SUPERUSER_CHOICES = [ ('TRUE', 'True'), ('False', 'False') ]
    #superuser = models.BooleanField(default=False, blank=True)
    #owner = models.BooleanField(default=False, blank=True) # a vendor relationship owner
    #vendor = models.BooleanField(default=False, blank=True) # a vendor user
    #analyst = models.BooleanField(default=False, blank=True) # an is_analyst
    #auditor = models.BooleanField(default=False, blank=True) # an auditor
    # notice the absence of a "Password field", that i, blank=Trues , blank=Tru, blank=Tru, blank=Trueeebuilt in.
    groups   = models.ManyToManyField(Group, blank=True, default=1, related_name='group')
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ ] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = User.objects.all().aggregate(largest=models.Max('order_id'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.order_id = last_id + 1
        super(User, self).save(*args, **kwargs)

class Company(models.Model):

    # fields
    #orderID = models.IntegerField(primary_key=True, null=False, editable=False, unique=True)
    order_id = models.IntegerField(default=1)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this Company.', editable=False, unique=True)
    #id = AutoFieldNonPrimary(unique=True)
    #Name = models.CharField(max_length=50, default='', help_text='Enter the Vendor Name')
    name = models.CharField(max_length=100, default='', help_text='Enter the Company Name', unique=True)
    address1 = models.CharField(max_length=200, default='', help_text='Enter the Company Address', blank=True)
    address2 = models.CharField(max_length=200, default='', blank=True)
    country = models.CharField(max_length=50, default='', help_text='Enter the country in which the Company is located', blank=True)
    city = models.CharField(max_length=50, default='', help_text='Enter the city in which the Company is located', blank=True)
    state = models.CharField(max_length=2, default='', help_text='Enter the state in which the Company is located', validators=[RegexValidator("^[A-Z]{2}$", "Invalid State Format")], blank=True)
    zip = models.CharField(max_length=10, default='', help_text='Enter the zip code', validators=[RegexValidator("^[0-9]{5}(?:-[0-9]{4})?$", "Invalid Zip Code Format")], blank=True)
    url = models.URLField(max_length=200, default='', help_text='Enter the Company URL', blank=True)
    logo = models.URLField(max_length=200, default='', help_text='Enter the URL where the Company Logo is located', blank=True)
    enrolled_date = models.DateField(default=datetime.date.today, help_text="Today's date", blank=True)
    relationship_owner = models.ForeignKey(User, related_name='relationship_owner', on_delete=models.CASCADE)
    RISK_RATING_CHOICES = [ ('LOW', 'Low'), ('MODERATE', 'Moderate'), ('HIGH', 'High') ]
    #RiskRating = models.CharField(max_length=12, choices=RISK_RATING_CHOICES, default='MODERATE')
    risk_rating = EnField(max_length=12, choices=RISK_RATING_CHOICES, default='MODERATE', blank=True)
    DATA_SENSITIVITY_RATING_CHOICES = [ ('LOW', 'Low'), ('MODERATE', 'Moderate'), ('HIGH', 'High') ]
    data_sensitivity_rating = EnField(max_length=12, choices=DATA_SENSITIVITY_RATING_CHOICES, default='MODERATE', blank=True)
    #employee = models.ManyToManyField('User', through='CompanyUsers', blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_vendor = models.BooleanField(default=True, blank=True)
    #relationship_age = FUTURE
    objects = CompanyManager()

    # Metadata
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
    # This means that the model isn't saved to the database yet
        if self._state.adding:

            # Get the maximum display_id value from the database
            last_id = Company.objects.all().aggregate(largest=models.Max('order_id'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.order_id = last_id + 1

        super(Company, self).save(*args, **kwargs)


class CompanyUsers(models.Model):
    Company = models.ForeignKey(Company, related_name='+', on_delete=models.CASCADE)
    User = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
