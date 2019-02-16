from __future__ import unicode_literals

import uuid as uuid

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone

from app import utils
from user.models import User

APP_PENDING = 'P'
APP_REJECTED = 'R'
APP_INVITED = 'I'
APP_LAST_REMIDER = 'LR'
APP_CONFIRMED = 'C'
APP_CANCELLED = 'X'
APP_ATTENDED = 'A'
APP_EXPIRED = 'E'

STATUS = [
    (APP_PENDING, 'Under review'),
    (APP_REJECTED, 'Wait listed'),
    (APP_INVITED, 'Invited'),
    (APP_LAST_REMIDER, 'Last reminder'),
    (APP_CONFIRMED, 'Confirmed'),
    (APP_CANCELLED, 'Cancelled'),
    (APP_ATTENDED, 'Attended'),
    (APP_EXPIRED, 'Expired'),
]

NO_ANSWER = 'NA'
MALE = 'M'
FEMALE = 'F'
OTHER = 'O'

GENDERS = [
    (NO_ANSWER, 'Prefer not to answer'),
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (OTHER, 'Other'),
]

D_NONE = 'None'
D_VEGETERIAN = 'Vegeterian'
D_VEGAN = 'Vegan'
D_HALAL = 'Halal'
D_LACTOSE_FREE = 'Lactose-free'
D_GLUTEN_FREE = 'Gluten-free'
D_OTHER = 'Others'

DIETS = [
    (D_NONE, 'No requirements'),
    (D_VEGETERIAN, 'Vegeterian'),
    (D_VEGAN, 'Vegan'),
    (D_HALAL, 'Halal'),
    (D_LACTOSE_FREE, 'Lactose-free'),
    (D_GLUTEN_FREE, 'Gluten-free'),
    (D_OTHER, 'Others')
]

S_FRONT_END = 'Dev Front-end'
S_BACK_END = 'Dev Back-end'
S_PRODUCT_MANAGER = 'Product Manager'
S_DESIGNER = 'Designer'
S_OTHER = 'Other'

SPECIALIZATIONS = [
    (S_FRONT_END, 'Dev Front-end'),
    (S_BACK_END, 'Dev Back-end'),
    (S_PRODUCT_MANAGER, 'Product Manager'),
    (S_DESIGNER, 'Designer'),
    (S_OTHER, 'Other')
]

H_FACEBOOK = 'Facebook'
H_FRIENDS = 'Friends'
H_EVENTBRITE = 'EventBrite'
H_Instagram = 'Instagram'
H_Twitter = 'Twitter'
H_OTHER = 'Other'

HEARD_FROM = [
    (H_FACEBOOK, 'Facebook'),
    (H_FRIENDS, 'Friends'),
    (H_EVENTBRITE, 'EventBrite'),
    (H_Instagram, 'Instagram'),
    (H_Twitter, 'Twitter'),
    (H_OTHER, 'Other')
]

TSHIRT_SIZES = [(size, size) for size in ('XS S M L XL XXL'.split(' '))]
DEFAULT_TSHIRT_SIZE = 'M'

YEARS = [(int(size), size) for size in ('2017 2018 2019 2020 2021 2022 2023 2024, 2025'.split(' '))]
DEFAULT_YEAR = 2019


class Application(models.Model):
    # META
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, primary_key=True)
    invited_by = models.ForeignKey(User, related_name='invited_applications', blank=True, null=True)

    # When was the application submitted
    submission_date = models.DateTimeField(default=timezone.now)
    # When was the last status update
    status_update_date = models.DateTimeField(blank=True, null=True)
    # Application status
    status = models.CharField(choices=STATUS, default=APP_PENDING,
                              max_length=2)

    # ABOUT YOU
    # Population analysis, optional
    gender = models.CharField(max_length=20, choices=GENDERS, default=NO_ANSWER)
    # Personal data (asking here because we don't want to ask birthday)
    under_age = models.BooleanField()
    nationality = models.CharField(max_length=50, null=True)

    specialization = models.CharField(choices=SPECIALIZATIONS,
                              max_length=20, null=True)

    skills = models.CharField(max_length=100, null=True)

    # Where is this person coming from?
    origin = models.CharField(max_length=300)

    # Is this your first hackathon?
    first_timer = models.BooleanField()
    expectations = models.TextField(max_length=500, blank=True, null=True)
    # Why do you want to come to X?
    description = models.TextField(max_length=500, blank=True, null=True)
    # Explain a little bit what projects have you done lately
    done_projects = models.TextField(max_length=500, blank=True, null=True)

    heard_from = models.CharField(choices=HEARD_FROM,
                              max_length=20)

    # Reimbursement
    reimb = models.BooleanField(default=False)
    reimb_amount = models.FloatField(blank=True, null=True, validators=[
        MinValueValidator(0, "Negative? Really? Please put a positive value")])

    # Giv me a resume here!
    resume = models.FileField(upload_to='resumes', null=True, blank=True)

    # University
    graduation_year = models.IntegerField(choices=YEARS, default=DEFAULT_YEAR)
    university = models.CharField(max_length=300)
    degree = models.CharField(max_length=300)

    # Info for swag and food
    diet = models.CharField(max_length=300, choices=DIETS, default=D_NONE)
    other_diet = models.CharField(max_length=600, blank=True, null=True)
    other_gender = models.CharField(max_length=600, blank=True, null=True)
    other_heard_from = models.CharField(max_length=600, blank=True, null=True)
    other_specialization = models.CharField(max_length=600, blank=True, null=True)
    tshirt_size = models.CharField(max_length=3, default=DEFAULT_TSHIRT_SIZE, choices=TSHIRT_SIZES)

    @classmethod
    def annotate_vote(cls, qs):
        return qs.annotate(vote_avg=Avg('vote__calculated_vote'))

    @property
    def uuid_str(self):
        return str(self.uuid)

    def get_soft_status_display(self):
        text = self.get_status_display()
        if "Not" in text or 'Rejected' in text:
            return "Pending"
        return text

    def __str__(self):
        return self.user.email

    def save(self, **kwargs):
        self.status_update_date = timezone.now()
        super(Application, self).save(**kwargs)

    def invite(self, user):
        # We can re-invite someone invited
        if self.status in [APP_CONFIRMED, APP_ATTENDED]:
            raise ValidationError('Application has already answered invite. '
                                  'Current status: %s' % self.status)
        self.status = APP_INVITED
        if not self.invited_by:
            self.invited_by = user
        self.last_invite = timezone.now()
        self.last_reminder = None
        self.status_update_date = timezone.now()
        self.save()

    def last_reminder(self):
        if self.status != APP_INVITED:
            raise ValidationError('Reminder can\'t be sent to non-pending '
                                  'applications')
        self.status_update_date = timezone.now()
        self.status = APP_LAST_REMIDER
        self.save()

    def expire(self):
        self.status_update_date = timezone.now()
        self.status = APP_EXPIRED
        self.save()

    def reject(self, request):
        if self.status == APP_ATTENDED:
            raise ValidationError('Application has already attended. '
                                  'Current status: %s' % self.status)
        self.status = APP_REJECTED
        self.status_update_date = timezone.now()
        self.save()

    def confirm(self):
        if self.status == APP_CANCELLED:
            raise ValidationError('This invite has been cancelled.')
        elif self.status == APP_EXPIRED:
            raise ValidationError('Unfortunately your invite has expired.')
        elif self.status in [APP_INVITED, APP_LAST_REMIDER]:
            self.status = APP_CONFIRMED
            self.status_update_date = timezone.now()
            self.save()
        elif self.status in [APP_CONFIRMED, APP_ATTENDED]:
            return None
        else:
            raise ValidationError('Unfortunately his application hasn\'t been '
                                  'invited [yet]')

    def cancel(self):
        if not self.can_be_cancelled():
            raise ValidationError('Application can\'t be cancelled. Current '
                                  'status: %s' % self.status)
        if self.status != APP_CANCELLED:
            self.status = APP_CANCELLED
            self.status_update_date = timezone.now()
            self.save()
            reimb = getattr(self.user, 'reimbursement', None)
            if reimb:
                reimb.delete()

    def check_in(self):
        self.status = APP_ATTENDED
        self.status_update_date = timezone.now()
        self.save()

    def is_confirmed(self):
        return self.status == APP_CONFIRMED

    def is_cancelled(self):
        return self.status == APP_CANCELLED

    def answered_invite(self):
        return self.status in [APP_CONFIRMED, APP_CANCELLED, APP_ATTENDED]

    def needs_action(self):
        return self.status == APP_INVITED

    def is_pending(self):
        return self.status == APP_PENDING

    def can_be_edit(self):
        return self.status == APP_PENDING and not self.vote_set.exists() and not utils.is_app_closed()

    def is_invited(self):
        return self.status == APP_INVITED

    def is_expired(self):
        return self.status == APP_EXPIRED

    def is_rejected(self):
        return self.status == APP_REJECTED

    def is_attended(self):
        return self.status == APP_ATTENDED

    def is_last_reminder(self):
        return self.status == APP_LAST_REMIDER

    def can_be_cancelled(self):
        return self.status == APP_CONFIRMED or self.status == APP_INVITED or self.status == APP_LAST_REMIDER

    def can_confirm(self):
        return self.status in [APP_INVITED, APP_LAST_REMIDER]
