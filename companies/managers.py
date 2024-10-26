from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth import hashers
from django.db.models import Q # new
from itertools import chain

class CompanyManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(name__icontains=query) |
                         Q(address1__icontains=query)|
                         Q(address2__icontains=query)|
                         Q(country__icontains=query)|
                         Q(state__icontains=query)|
                         Q(zip__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs

class UserManager(BaseUserManager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(first_name__icontains=query) |
                         Q(last_name__icontains=query)|
                         Q(usercompany__name__icontains=query)|
                         Q(email__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs

    #def create_user(self, email, password =None, is_active=True, is_staff=True, is_admin=False, is_superuser=False, is_owner=False, is_vendor=False, is_analyst=False, is_auditor=False):
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        #print("yep. the Create_user is called. ... so now i'm completely lost")
        if not email:
            raise ValueError('Users must have an email address')

        #user_obj = self.model(
        #    email=self.normalize_email(email),
        #)
        #print("password will be set to -" + str(password))

        ### this is where we have to debug the superuser problem
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        #user_obj.staff = is_staff
        #user_obj.admin = is_admin
        #user_obj.vendor = is_vendor
        #user_obj.analyst = is_analyst
        #user_obj.auditor = is_auditor
        #user_obj.owner = is_owner
        #is_superuser = False
        #user_obj.superuser = is_superuser
        #user_obj.save(using=self._db)
        user.save()
        return user

    #def create_staffuser(self, email, password=None, is_active=True, is_staff=True, is_admin=False, is_superuser=False, is_owner=False, is_vendor=False, is_analyst=False, is_auditor=False):
    #    """
    #    Creates and saves a staff user with the given email and password.
    #    """
    #    print("yep. the Create_staffuser is called. ... so now i'm completely lost")
    #    user = self.create_user(
    #        email,
    #        password=password,
    #    )
    #    user.staff = True
    #    user.save(using=self._db)
    #    return user

    #def create_superuser(self, email, password=None, is_active=True, is_staff=False, is_admin=True, is_owner=True, is_vendor=False, is_analyst=True, is_auditor=True):
    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        #print("yep. the Create_superuser is called. ... so now i'm completely lost")
        #user = self.create_user(
        #    email,
        #    password=password,
        #)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)



class CustomUserManager(BaseUserManager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(first_name__icontains=query) |
                         Q(last_name__icontains=query) |
                         Q(username__icontains=query) |
                         Q(email__icontains=query)|
                         Q(address1__icontains=query)|
                         Q(address2__icontains=query)|
                         Q(country__icontains=query)|
                         Q(state__icontains=query)|
                         Q(zip__icontains=query) |
                         Q(department__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs

    def create_user(
            self, email, first_name, last_name, password=None,
            commit=True):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        print("yep. the Create_user [in CustomUserManager] is called. ... so now i'm completely lost")
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        hashed_password = hashers.make_password(password)
        print("hashing the password: " + str(hashed_password))
        user.set_password(hashed_password)
        #user.set_password(self.cleaned_data["password"])
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        print("yep. the Create_superuser [in CustomUserManager] is called. ... so now i'm completely lost")
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
