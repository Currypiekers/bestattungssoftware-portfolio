from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from djstripe.exceptions import MultipleSubscriptionException
from djstripe.models import Customer, Plan
from stripe.error import AuthenticationError
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from tenant_schemas.models import TenantMixin
from django.contrib.auth.models import UserManager

from logging import getLogger
logger = getLogger(__name__)


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        from .models import Company
        company, created = Company.objects.get_or_create(id=1, defaults={'name': 'bestatter'})
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('company_id', company.id)   

        return self._create_user(username, email, password, **extra_fields)

class Company(TenantMixin):
    inhaber_vorname = models.CharField(max_length=100, null=True, blank=True)
    inhaber_nachname = models.CharField(max_length=100, null=True, blank=True)
    unternehmensname = models.CharField(max_length=100, null=True, blank=True)
    unternehmensform = models.CharField(max_length=100, null=True, blank=True)
    UstIdNr = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='company_logo/', null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    strasse = models.CharField(max_length=255, null=True, blank=True)
    plz = models.CharField(max_length=10, null=True, blank=True)
    ort = models.CharField(max_length=100, null=True, blank=True)
    paid_until = models.DateField(null=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    header_text = models.TextField(null=True, blank=True)
    footer_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class BankAccount(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='bank_accounts')
    name = models.CharField(max_length=255, verbose_name="Kontoname")
    iban = models.CharField(max_length=255, verbose_name="IBAN")
    bic = models.CharField(max_length=255, blank=True, null=True, verbose_name="BIC")

    def __str__(self):
        return f"{self.name} - {self.iban}"
    
class EmailSettings(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='email_settings')
    email_backend = models.CharField(max_length=255, default='django.core.mail.backends.smtp.EmailBackend')
    email_host = models.CharField(max_length=255, blank=True, null=True)
    email_port = models.IntegerField(blank=True, null=True)
    email_host_user = models.CharField(max_length=255, blank=True, null=True)
    email_host_password = models.CharField(max_length=255, blank=True, null=True)
    email_use_tls = models.BooleanField(default=True)
    email_use_ssl = models.BooleanField(default=False)
    default_from_email = models.EmailField(max_length=254, blank=True, null=True)

    def __str__(self):
        return f"Email Settings for {self.company.name}"


class CustomUser(AbstractUser):

    ROLES = (
        ('Geschäftsführer', 'Geschäftsführer'),
        ('Mitarbeiter', 'Mitarbeiter'),
        ('Kunde', 'Kunde'),
    )
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active', null=True, blank=True)
    objects = CustomUserManager()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLES, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    mitarbeiter_kuerzel = models.CharField(max_length=2, null=True, blank=True)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_users'  # Add a related_name argument
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_users'  # Add a related_name argument
    )

    def __str__(self):
        return self.username
    
    

    

    
    @property
    def bypassing_stripe(self):
        """Checks if BYPASS_STRIPE is set to True in settings"""
        return settings.BYPASS_STRIPE

    @cached_property
    def customer(self):
        try:
            customer, _ = Customer.get_or_create(self)
            return customer
        except AuthenticationError as e:
            # if we are bypassing stripe, we swallow the exception and
            # emit a warning instead. This allows us to develop the app
            # without caring about setting up stripe for every development
            # environment
            if settings.BYPASS_STRIPE:
                logger.warning(
                    "Warning: You are using an invalid Stripe API key. Since BYPASS_STRIPE is set to True, this "
                    "error is ignored. To test your Stripe integration, make sure to set BYPASS_STRIPE to False."
                )
                return None
            raise e

    @cached_property
    def has_active_subscription(self):
        """Checks if a user has an active subscription."""
        try:
            return self.customer.subscription is not None
        except MultipleSubscriptionException:
            return True
        except AttributeError as e:
            # if BYPASS_STRIPE is set to True, our customer object has no
            # subscription (it is None). Setting BYPASS_STRIPE to True
            # allows us to test the app, without setting up Stripe for
            # every development environment
            if settings.BYPASS_STRIPE:
                return True
            raise e

    @cached_property
    def invoices(self):
        return self.customer.invoices.all()

    @property
    def is_trialling(self):
        return not self.has_active_subscription and self.trial_ends_at > timezone.now()

    @property
    def trial_ends_at(self):
        return self.date_joined + timezone.timedelta(days=settings.TRIAL_DAYS)

    @cached_property
    def plan(self):
        # if BYPASS_STRIPE is set to True, we simply return the trial
        # plan. This allows us to test the app without setting up
        # stripe for every development environment
        if settings.BYPASS_STRIPE:
            logger.warning(
                "Warning: Bypassing Stripe integration since BYPASS_STRIPE is set to True. \n"
                "To test your Stripe integration, make sure to set up BYPASS_STRIPE to False.\n"
                "Learn more at: https://getlaunchr.com/docs/payments/"
            )
            return settings.PLANS[settings.TRIAL_PLAN_KEY]
        if self.stripe_plan:
            return self.get_plan_by_stripe_id(
                self.stripe_plan.id
            )
        return None

    @cached_property
    def stripe_plan(self):
        if self.has_active_subscription:
            try:
                return self.customer.subscription.plan
            except MultipleSubscriptionException:
                return self.customer.subscriptions.latest().plan
        if self.is_trialling:
            return Plan.objects.get(
                id=self.get_stripe_plan_id_by_key(settings.TRIAL_PLAN_KEY)
            )
        return None

    def can_use_feature(self, feature_key):
        if self.plan:
            for feature in self.plan.get('features', []):
                if feature['key'] == feature_key:
                    return feature['enabled']
            plan_uuid = self.get_plan_by_stripe_id(self.plan.id)
            raise ImproperlyConfigured(
                f"Unable to find the feature with feature_key '{feature_key}' for the plan \n"
                f"with the uuid '{plan_uuid}'. Make sure to add it to the features list in \n"
                f"your settings.\n"
                f"See: https://getlaunchr.com/docs/subscriptions/#can_use_feature"
            )
        return False

    @staticmethod
    def get_plan_by_stripe_id(stripe_id):
        for plan in settings.PLANS.values():
            if plan['stripe_id'] == stripe_id:
                return plan
        raise ImproperlyConfigured(
            f"Unable to find a configured plan for the stripe_id '{stripe_id}'.\n"
            f"Make sure to add the 'stripe_id' to one of your plans in your settings.\n"
            f"See: https://getlaunchr.com/docs/subscriptions/#get_plan_by_stripe_id"
        )

    @staticmethod
    def get_stripe_plan_id_by_key(plan_key):
        stripe_id = settings.PLANS.get(plan_key, {}).get('stripe_id', None)
        if not stripe_id:
            raise ImproperlyConfigured(
                f"Unable to get the stripe_id for the plan with the key '{plan_key}'.\n"
                f"Make sure to set the 'stripe_id' in your settings correctly.\n"
                f"See: https://getlaunchr.com/docs/subscriptions/#get_stripe_plan_id_by_key"
            )
        return stripe_id